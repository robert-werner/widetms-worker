import ssl

from celery import Celery
from config.environment import CELERY_RESULT_URL, CELERY_BROKER_URL

app = Celery('widetms.worker', broker=CELERY_BROKER_URL, backend=CELERY_RESULT_URL)

app.conf.update(
    task_serializer='pickle',
    result_serializer='pickle',
    accept_content=['pickle']
)