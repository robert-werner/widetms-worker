import os

CELERY_BROKER_URL = os.environ['CELERY_BROKER_URL']
CELERY_RESULT_URL = os.environ['CELERY_RESULT_URL']
SOURCE_STORAGE = os.environ['TARGET_SOURCE_STORAGE']
