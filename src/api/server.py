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
def selenium_search() -> str:
    """Runs Selenium search for item"""
    run_search("Breguet", "1200", "17650")


@server.route("/refresh", methods=["GET"])
def add_search_to_queue():
    """Adds search task to Celery queue"""
    print(f"selenium_search() added to queue", file=sys.stderr)
    task = selenium_search.apply_async() # task = get_number_task.apply_async(args=[pipeline_run])
    return task.id


if __name__ == "__main__":
    server.run(host="0.0.0.0", port=port)