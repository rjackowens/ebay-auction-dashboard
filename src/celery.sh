#!/bin/sh
/usr/local/bin/celery -A server worker --pool=prefork --loglevel=INFO