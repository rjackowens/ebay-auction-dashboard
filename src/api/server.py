import os, sys
import pandas as pd
from flask import Flask
from celery import Celery
from selenium_scraper import Scraper


server, port= Flask(__name__), 9000

server.config["CELERY_BROKER_URL"] = os.getenv("celery_broker_url")
server.config["CELERY_RESULT_BACKEND"] = os.getenv("celery_broker_url")

celery = Celery("server", broker=server.config["CELERY_BROKER_URL"])
celery.conf.update(server.config)


@celery.task() # @celery.task(rate_limit='20/m') 
def selenium_auction_search(title: str, min_price: str, max_price: str) -> str:
    """Runs Selenium auction search for item"""
    Scraper().run_auction_search(title, min_price, max_price)


@celery.task() # @celery.task(rate_limit='20/m') 
def selenium_bit_search(title: str, min_price: str, max_price: str) -> str:
    """Runs Selenium buy it now search for item"""
    Scraper().run_bit_search(title, min_price, max_price)


@server.route("/auction-refresh", methods=["GET"])
def add_auction_searches_to_queue():
    """Adds all auction search tasks to Celery queue"""
    df = pd.read_csv("search_templates/watch_list_short.csv", index_col=0)

    for index, row in df.iterrows():
        task = selenium_auction_search.apply_async(args=[index, row['MIN PRICE'], row['MAX PRICE']])

    return task.id


@server.route("/bit-refresh", methods=["GET"])
def add_bit_searches_to_queue():
    """Adds all buy it now search tasks to Celery queue"""
    df = pd.read_csv("search_templates/watch_test.csv", index_col=0)

    for index, row in df.iterrows():
        task = selenium_bit_search.apply_async(args=[index, row['MIN PRICE'], row['MAX PRICE']])

    return task.id


if __name__ == "__main__":
    server.run(host="0.0.0.0", port=port)
