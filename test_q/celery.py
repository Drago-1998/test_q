import os

from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'test_q.settings')

app = Celery('test_q')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
