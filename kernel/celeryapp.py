import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kernel.settings.development')

celery_app = Celery('kernel')

celery_app.config_from_object('django.conf:settings', namespace='CELERY')

celery_app.autodiscover_tasks()

celery_app.conf.beat_schedule = {
    'contact_daily_notification': {
        'task': 'contacts.tasks.send_contact_daily_notification',
        'schedule': crontab(hour="0", minute="0"),
    },
}
