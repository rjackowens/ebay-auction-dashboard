import os, sys, time, subprocess, redis, requests, json
from flask import Flask, request, url_for, jsonify, render_template
from celery import Celery

requests.urllib3.disable_warnings()
server, port= Flask(__name__), 8080

server.config["CELERY_BROKER_URL"] = os.getenv("celery_broker_url")
server.config["CELERY_RESULT_BACKEND"] = os.getenv("celery_broker_url")
server.config["TEMPLATES_AUTO_RELOAD"] = True # https://stackoverflow.com/questions/37575089/disable-template-cache-jinja2

celery = Celery("server", broker=server.config["CELERY_BROKER_URL"])
celery.conf.update(server.config)


def run_shell(command: str) -> subprocess.CompletedProcess:
    """Runs arbitrary shell command"""
    try:
        return subprocess.check_output(command, shell=True)
    except subprocess.CalledProcessError as e:
        print(e.returncode, e.output)
        raise


def ocp_login() -> None:
    """Logs in to OpenShift using automation_token"""
    oc_login_command = f"oc login --insecure-skip-tls-verify --server={os.getenv('openshift_cluster_url')} --token={os.getenv('automation_token')}"
    run_shell(oc_login_command)
    print("successfully logged in to OpenShift", file=sys.stderr)


def get_pipeline_status(pipeline_run) -> str:
    """Filter results of tkn pipelinerun describe to find pipeline status"""
    tkn_status_command = f"o=$(tkn pipelinerun describe {pipeline_run}) && t=$(echo \"$o\" | grep -A 1 STATUS | head -2 | tail -1 | awk '{{print $5}}') && echo $t"
    result = run_shell(tkn_status_command).decode('utf-8').strip('\n')

    if str(result) == "minute" or str(result) == "minutes": # index must be increased after 1 minute run duration
        tkn_status_command = f"o=$(tkn pipelinerun describe {pipeline_run}) && t=$(echo \"$o\" | grep -A 1 STATUS | head -2 | tail -1 | awk '{{print $6}}') && echo $t"
        result = run_shell(tkn_status_command).decode('utf-8').strip('\n')

    return result


def send_teams_status(pipeline_run: str, status: str) -> None:
    """Sends status to Teams channel incoming webhook"""
    teams_url = os.getenv("teams_webhook_url")

    if status == "start":
        message = f"<b>STARTED:</b> {pipeline_run} <a href='{os.getenv('openshift_logs_url')}{pipeline_run}/logs'>. View logs</a>"
    elif status == "success":
        message = f"<div style='display: inline; color: #fcd303'> &#9745 </div> <b>SUCCESS:</b> {pipeline_run} <a href='{os.getenv('openshift_logs_url')}{pipeline_run}/logs'>. View logs</a>"
    elif status == "timeout":
        message = f"<div style='display: inline; color: #eb7d34'> &#9830 </div> <b>TIMEOUT:</b> {pipeline_run} <a href='{os.getenv('openshift_logs_url')}{pipeline_run}/logs'>. View logs</a>"
    elif status == "failure":
        message = f"<div style='display: inline'> &#9888 </div> <b>FAILED:</b> {pipeline_run} <a href='{os.getenv('openshift_logs_url')}{pipeline_run}/logs'>. View logs</a>"

    payload, headers = json.dumps({
        "text": f"{message}"
    }), {"Content-Type": "application/json"}

    requests.request("POST", teams_url, headers=headers, data=payload, verify=False)


@celery.task
def check_status_loop(pipeline_run: str) -> str:
    """Checks pipeline status every 10 seconds, sends Teams notification on success/failure"""
    ocp_login()
    i, timeout = 0, 570 # 30 second offset to give pipeline time to start

    while i < timeout:

        status = get_pipeline_status(pipeline_run)

        if status == "Running":
            print(f"{pipeline_run} is still running. Waiting {timeout - i} more seconds", file=sys.stderr)
            i += 10
            time.sleep(10)

        elif status == "Succeeded":
            print(f"{pipeline_run} succeeded", file=sys.stderr)
            send_teams_status(pipeline_run, "success")
            return f"{pipeline_run} succeeded"

        else:
            print(f"{pipeline_run} failed", file=sys.stderr)
            send_teams_status(pipeline_run, "failure")
            return f"{pipeline_run} failed"

    send_teams_status(pipeline_run, "timeout")
    return f"{pipeline_run} timed out"


from dummy_data import build_4
from mongo import get_items
@server.route('/')
def table_test():
    return render_template(
        'dashboard_4.html',
        build_1=get_items("build_1"),
        build_2=get_items("build_2"),
        build_3=get_items("build_3"),
        build_4=build_4
        )


@server.route('/db_refresh')
def db_refresh():
    """Trigger update of DB by re-running all Celery tasks """
    print("REFRESHING!!!!!!!!!!!!!!!!!!!", file=sys.stdout)
    return "placeholder"


@server.route("/status", methods=["POST"])
def trigger_teams_status_task():
    """Adds Teams event loop task to Celery queue"""
    pipeline_run = request.get_json()["pipeline_run_name"] # default flask.Request object

    print(f"{pipeline_run} added to queue", file=sys.stderr)
    send_teams_status(f"{pipeline_run}", "start")
    task = check_status_loop.apply_async(args=[pipeline_run])

    return task.id


@server.route("/status/<task_id>", methods=["GET"])
def get_task_status(task_id: str):
    """Gets current status of Celery task"""
    task = check_status_loop.AsyncResult(task_id)

    if task.state == "PENDING":
        response = {
            "state": task.state,
            "status": "Build is still running..."
        }

    elif task.state != "FAILURE":
        response = {
            "state": "Completed.",
            "status": "Task has completed..."
        }

        if "result" in task.info:
            response["result"] = task.info["result"]

    else:
        # something went wrong in the background job
        response = {
            "state": task.state,
            "status": str(task.info),  # this is the exception raised
        }

    return jsonify(response)


if __name__ == "__main__":
    from mongo import init_connection, populate_dummy_data
    init_connection()
    populate_dummy_data() # populates build_1-3 collections
    server.run(host="0.0.0.0", port=port)
