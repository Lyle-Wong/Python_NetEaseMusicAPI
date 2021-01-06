import logging

from celery import Celery
from celery.schedules import crontab

logging.basicConfig(level=logging.INFO,
                format='%(asctime)s %(filename)s [line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S')


broker = 'amqp://user:bitnami@stats:5672/solr'
backend = 'redis://redis:6379/0'


# set the default Django settings module for the 'celery' program.
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'netease.settings')

# from django.conf import settings  # noqa

celery_app = Celery('search_event', broker=broker, backend=backend, include=['async_tasks.celery_tasks'])

celery_app.conf.update(
    result_expires=3600,
    timezone='Asia/Shanghai',
    enable_utc=True,
    beat_schedule={
        "signin_msg_1": {
            "task": "celery_app.signin",
            "schedule": crontab(minute=0, hour=7)
        },
        "signin_msg_2": {
            "task": "celery_app.signin",
            "schedule": crontab(minute=30, hour=18)
        }
    }
)
