"""Configuration for Celery.

Logging and Settings for Celery are all handled here.
"""

import logging
import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "snoop.defaultsettings")

app = Celery('snoop.data')
app.conf.update(
    worker_log_format="[%(asctime)s: %(name)s %(levelname)s] %(message)s",
)
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# from pprint import pprint
# pprint(logging.Logger.manager.loggerDict)
logging.getLogger('celery').setLevel(logging.INFO)
