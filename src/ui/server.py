import os, sys, time, redis, requests, json
from mongo import get_items
from flask import Flask, request, url_for, jsonify, render_template, redirect

requests.urllib3.disable_warnings()
server, port= Flask(__name__), 8080

server.config["TEMPLATES_AUTO_RELOAD"] = True # https://stackoverflow.com/questions/37575089/disable-template-cache-jinja2


@server.route('/') # auctions
def render_auctions():
    return render_template(
        'auctions.html',
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
        grand_seiko=get_items("grand seiko"),
        longines=get_items("longines"),
        parmigiani=get_items("parmigiani"),
        piaget=get_items("piaget"),
        porsche_design=get_items("porsche design"),
        glashutte_original=get_items("glashutte original"),
        alain_silberstein=get_items("alain silberstein"),
        alpina=get_items("alpina"),
        bremont=get_items("bremont"),
        carlo_ferrara=get_items("carlo ferrara"),
        concord=get_items("concord"),
        dubey_schaldenbrand=get_items("dubey schaldenbrand"),
        hamilton=get_items("hamilton"),
        ikepod=get_items("ikepod"),
        jaquet_droz=get_items("jaquet droz"),
        jean_d_eve=get_items("jean d'eve"),
        rado=get_items("rado"),
        sevenfriday=get_items("sevenfriday"),
        ulysse_nardin=get_items("ulysse nardin"),
        vulcain=get_items("vulcain"),
        zodiac=get_items("zodiac")
        )


@server.route('/bit') # buy it now
def render_buy_it_now():
    return render_template(
        'buy_it_now.html',
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
        grand_seiko=get_items("grand seiko"),
        longines=get_items("longines"),
        parmigiani=get_items("parmigiani"),
        piaget=get_items("piaget"),
        porsche_design=get_items("porsche design"),
        glashutte_original=get_items("glashutte original"),
        alain_silberstein=get_items("alain silberstein"),
        alpina=get_items("alpina"),
        bremont=get_items("bremont"),
        carlo_ferrara=get_items("carlo ferrara"),
        concord=get_items("concord"),
        dubey_schaldenbrand=get_items("dubey schaldenbrand"),
        hamilton=get_items("hamilton"),
        ikepod=get_items("ikepod"),
        jaquet_droz=get_items("jaquet droz"),
        jean_d_eve=get_items("jean d'eve"),
        rado=get_items("rado"),
        sevenfriday=get_items("sevenfriday"),
        ulysse_nardin=get_items("ulysse nardin"),
        vulcain=get_items("vulcain"),
        zodiac=get_items("zodiac")
        )


@server.route('/auction-db-refresh', methods=["GET"])
def auction_db_refresh():
    """Trigger auction update of DB by re-running all Celery tasks """
    print("refreshing auction searches...", file=sys.stdout)
    # return redirect('http://localhost:9000/refresh', code=307) # preserves GET method instead of OPTIONS
    request = requests.get("http://status-dashboard-api:9000/auction-refresh")
    return request.text


@server.route('/bit-db-refresh', methods=["GET"])
def bit_db_refresh():
    """Trigger buy it now update of DB by re-running all Celery tasks """
    print("refreshing auction searches...", file=sys.stdout)
    # return redirect('http://localhost:9000/refresh', code=307) # preserves GET method instead of OPTIONS
    request = requests.get("http://status-dashboard-api:9000/bit-refresh")
    return request.text


if __name__ == "__main__":
    server.run(host="0.0.0.0", port=port)
