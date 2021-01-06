import json
import logging
import os

import requests
from requests.models import HTTPError

from .celery import celery_app


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
