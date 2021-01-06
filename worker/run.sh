#!/bin/bash
# pipenv run python async_tasks/ap_task.py

pipenv run celery -A async_tasks.celery worker -B --loglevel=INFO