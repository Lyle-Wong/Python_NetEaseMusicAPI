import logging

from celery import Celery

logging.basicConfig(level=logging.INFO,
                format='%(asctime)s %(filename)s [line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S')



# set the default Django settings module for the 'celery' program.
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'netease.settings')

# from django.conf import settings  # noqa

celery_app = Celery('search_event')

celery_app.config_from_object("async_tasks.celeryconfig")
