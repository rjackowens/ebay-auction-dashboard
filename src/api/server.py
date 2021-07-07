import os, sys
from flask import Flask
from celery import Celery
from selenium_scraper import get_number

server, port= Flask(__name__), 9000

server.config["CELERY_BROKER_URL"] = os.getenv("celery_broker_url")
server.config["CELERY_RESULT_BACKEND"] = os.getenv("celery_broker_url")
server.config["TEMPLATES_AUTO_RELOAD"] = True # https://stackoverflow.com/questions/37575089/disable-template-cache-jinja2

celery = Celery("server", broker=server.config["CELERY_BROKER_URL"])
celery.conf.update(server.config)


@celery.task() # @celery.task(rate_limit='20/m') 
def get_number_task() -> str:
    """Gets a random number from webpage"""
    get_number()


@server.route("/get_number", methods=["GET"])
def trigger_teams_status_task():
    """Adds task to Celery queue"""
    print(f"get_number() added to queue", file=sys.stderr)
    task = get_number_task.apply_async() # task = get_number_task.apply_async(args=[pipeline_run])
    return task.id


if __name__ == "__main__":
    server.run(host="0.0.0.0", port=port)