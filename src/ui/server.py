import os, sys, time, redis, requests, json
from flask import Flask, request, url_for, jsonify, render_template

requests.urllib3.disable_warnings()
server, port= Flask(__name__), 8080

server.config["TEMPLATES_AUTO_RELOAD"] = True # https://stackoverflow.com/questions/37575089/disable-template-cache-jinja2


from dummy_data import build_4
from mongo import get_items
@server.route('/')
def table_test():
    return render_template(
        'dashboard_4.html',
        zenith=get_items("zenith"),
        sinn=get_items("sinn"),
        jaeger_lecoultre=get_items("jaeger lecoultre"),
        breguet=get_items("breguet"),
        girard_perregaux=get_items("girard perregaux"),
        chopard=get_items("chopard"),
        universal_geneve=get_items("universal geneve"),
        iwc=get_items("iwc"),
        vacheron_constantin=get_items("vacheron constantin"),
        omega=get_items("omega"),
        nomos=get_items("nomos"),
        bell_and_ross=get_items("bell & ross"),
        breitling=get_items("breitling"),
        cartier=get_items("cartier"),
        tudor=get_items("tudor"),
        grand_seiko=get_items("grand seiko")
        )


@server.route('/db_refresh')
def db_refresh():
    """Trigger update of DB by re-running all Celery tasks """
    print("REFRESHING!!!!!!!!!!!!!!!!!!!", file=sys.stdout)
    return "placeholder"


if __name__ == "__main__":
    # from mongo import init_connection, populate_dummy_data
    # init_connection()
    # populate_dummy_data() # populates build_1-3 collections
    server.run(host="0.0.0.0", port=port)
