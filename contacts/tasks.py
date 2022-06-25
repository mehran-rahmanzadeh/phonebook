from celery import shared_task
from celery.utils.log import get_task_logger
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mass_mail
from django.db.models import Count

logger = get_task_logger(__name__)


@shared_task
def send_contact_daily_notification():
    """send email to all users each day
    email contains count of contacts in yesterday and today
    """
    mails = tuple()
    subject = "Contacts count notification =)"
    email_from = settings.DEFAULT_FROM_EMAIL
    objs_to_update = []
    for u in get_user_model().actives.annotate(contacts_count=Count('contacts')).iterator():
        if u.email:
            yesterday_count = u.last_day_contact_count
            today_count = u.contacts_count
            message = f'yesterday: {yesterday_count}, today: {today_count}'
            mails += ((subject, message, email_from, [u.email]),)  # add to mass email payload
            u.last_day_contact_count = today_count  # update last day's contact count
            objs_to_update.append(u)  # add to bulk_update list
        else:  # ignore if user has no email
            today_count = u.contacts.count()
            u.last_day_contact_count = today_count
            objs_to_update.append(u)

    # send mass emails chunk by chunk using Celery (check EMAIL_BACKEND for more detail)
    send_mass_mail(mails)
    logger.info(f"{len(mails)} emails sent to users")

    # update all user's last_day_contact_count
    get_user_model().objects.bulk_update(objs_to_update, ['last_day_contact_count'])