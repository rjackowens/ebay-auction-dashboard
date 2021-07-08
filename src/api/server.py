import os, sys
import pandas as pd
from flask import Flask
from celery import Celery
from selenium_scraper import run_search

server, port= Flask(__name__), 9000

server.config["CELERY_BROKER_URL"] = os.getenv("celery_broker_url")
server.config["CELERY_RESULT_BACKEND"] = os.getenv("celery_broker_url")

celery = Celery("server", broker=server.config["CELERY_BROKER_URL"])
celery.conf.update(server.config)


@celery.task() # @celery.task(rate_limit='20/m') 
def selenium_search(title: str, min_price: str, max_price: str) -> str:
    """Runs Selenium search for item"""
    run_search(title, min_price, max_price)


@server.route("/refresh", methods=["GET"])
def add_searches_to_queue():
    """Adds all search tasks to Celery queue"""
    df = pd.read_csv("watch_list.csv", index_col=0)

    for index, row in df.iterrows():
        task = selenium_search.apply_async(args=[index, row['MIN PRICE'], row['MAX PRICE']])

    return task.id


if __name__ == "__main__":
    server.run(host="0.0.0.0", port=port)