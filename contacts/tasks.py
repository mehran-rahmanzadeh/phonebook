from celery import shared_task
from celery.utils.log import get_task_logger
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail

logger = get_task_logger(__name__)


@shared_task
def notify_user(user):
    """send mail to user"""
    user = get_user_model().objects.get(id=user)
    email_to = user.email
    email_from = settings.DEFAULT_FROM_EMAIL
    yesterday_count = user.last_day_contact_count
    today_count = user.contacts.count()
    text = f'yesterday: {yesterday_count}, today: {today_count}'
    user.last_day_contact_count = today_count
    user.save()
    send_mail("Contacts count notification =)", text, email_from, [email_to])
    logger.info(f"Contact count notify user: {user.sku}")


@shared_task
def send_contact_daily_notification():
    """send email to all users each day
    email contains count of contacts in yesterday and today
    """
    for u in get_user_model().objects.iterator():
        if u.email:
            notify_user.delay(user=u.id)
        else:
            continue
