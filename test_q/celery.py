import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'test_q.settings')

app = Celery('test_q')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'import-data-every-minute': {
        'task': 'order.tasks.import_data',
        'schedule': crontab()
    },
    'update-currency-every-day': {
        'task': 'order.tasks.update_currency',
        'schedule': crontab(hour=8)
    },
}
