import os
import logging
from celery import Celery
from celery.signals import setup_logging
from django_structlog.celery.steps import DjangoStructLogInitStep
from kombu import Queue

from config.settings import LOGGING, TIME_ZONE

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

@setup_logging.connect
def receiver_setup_logging(loglevel, logfile, format, colorize, **kwargs):
    logging.config.dictConfig(LOGGING)

celery_app = Celery()
celery_app.steps['worker'].add(DjangoStructLogInitStep)

celery_app.conf.update(
    control_exchange='backend.celery',
    event_exchange='backend.celeryev',
    event_queue_prefix='backend.celeryev',
    task_create_missing_queues=False,
    task_default_queue='backend.tasks.default',
    task_default_exchange='backend.tasks',
    task_default_routing_key='default',
    task_queues=[
        Queue('backend.tasks.default', exchange='backend.tasks', routing_key='default', no_declare=True),
        Queue('backend.public.default', exchange='backend.public', routing_key='default', no_declare=True),
    ],
    task_routes={
        'apps.*': {
            'exchange': 'backend.tasks',
            'routing_key': 'default',
        },
        'celery.*': {
            'queue': 'backend.tasks',
            'routing_key': 'default',
        },
        'public.*': {
            'queue': 'backend.public',
            'routing_key': 'default',
        },
    },
    timezone=TIME_ZONE
)

celery_app.autodiscover_tasks()
