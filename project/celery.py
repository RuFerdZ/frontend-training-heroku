import os

from celery import Celery

# Set the default Django settings module for the 'celery' program.
from project.settings import ENABLE_CELERY

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

if ENABLE_CELERY:
    app = Celery('project')

    # - namespace='CELERY' means all celery-related configuration keys
    #   should have a `CELERY_` prefix.
    app.config_from_object('django.conf:settings', namespace='CELERY')

    # Load task modules from all registered Django apps.
    app.autodiscover_tasks()
