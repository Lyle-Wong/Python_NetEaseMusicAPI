import os

from celery import Celery

from requests.models import HTTPError
import requests
import os
import logging
import json

logging.basicConfig(level=logging.INFO,
                format='%(asctime)s %(filename)s [line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S')


broker = 'amqp://user:bitnami@stats:5672/solr'
backend = 'redis://redis:6379/0'


# set the default Django settings module for the 'celery' program.
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'netease.settings')

# from django.conf import settings  # noqa

celery_app = Celery('search_event', broker=broker, backend=backend)

celery_app.conf.update(
    result_expires=3600,
)

@celery_app.task
def signin():
    nginx_host = os.environ.get('NGINX')
    logging.info('nginx host:'  + nginx_host)
    base_url = f'http://{nginx_host}/api/'
    resp = requests.get(base_url + 'user/status')
    if resp.status_code != 200:
        email = os.environ.get('MUSIC_EMAIL')
        password = os.environ.get('MUSIC_PASSWORD')
        requests.get(base_url + f'user/login?email={email}&password={password}')
    resp = requests.get(base_url + 'user/status')
    if resp.status_code != 200:
        logging.error('failed to login')
        raise HTTPError
    requests.get(base_url + 'user/signin')
    resp = requests.get(base_url + 'user/level')
    logging.info('current level:' + json.dumps(json.loads(resp.text), indent=2))

    trigger_task_resp = requests.get(base_url + 'tasks/task')
    logging.info(trigger_task_resp.text)
    logging.info('current level:' + json.dumps(json.loads(trigger_task_resp.text), indent=2))
    resp = requests.get(base_url + 'user/level')
    logging.info('after task level:' + json.dumps(json.loads(resp.text), indent=2))

# Using a string here means the worker will not have to
# pickle the object when using Windows.
# celery_app.config_from_object('django.conf:settings')
# celery_app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


# if __name__ == "__main__":
#     celery_app.start()
