#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2021-01-06 19:35:13
# @Author  : Your Name (you@example.org)
# @Link    : link
# @Version : 1.0.0

import os
from celery.schedules import crontab

broker_url = 'amqp://user:bitnami@stats:5672/solr'
result_backend = 'redis://redis:6379/0'

task_serializer = 'json'
result_serializer = 'json'
accept_content = ['json']

result_expires=3600
timezone='Asia/Shanghai'
enable_utc=True

imports = [
    "async_tasks.celery_tasks",
]

beat_schedule={
        "signin_task_1": {
            "task": "async_tasks.celery_tasks.signin",
            "schedule": crontab(minute=0, hour=7),
            "args": ()
        },
        "signin_task_2": {
            "task": "async_tasks.celery_tasks.signin",
            "schedule": crontab(minute=30, hour=18),
            "args": ()
        },
        "signin_task_3": {
            "task": "async_tasks.celery_tasks.signin",
            "schedule": crontab(minute="*/1"),
            "args": ()
        }
    }