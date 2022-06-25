from celery import shared_task
from celery.utils.log import get_task_logger
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mass_mail
from django.db.models import Count

from contacts.models import Contact, PhoneNumber
from contacts.utils import merge_qs

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
            today_count = u.contacts_count
            u.last_day_contact_count = today_count
            objs_to_update.append(u)

    # send mass emails chunk by chunk using Celery (check EMAIL_BACKEND for more detail)
    send_mass_mail(mails)
    logger.info(f"{len(mails)} emails sent to users")

    # update all user's last_day_contact_count
    get_user_model().objects.bulk_update(objs_to_update, ['last_day_contact_count'])


@shared_task
def find_duplicates_and_merge():
    """
    find duplicate records in Contact and merge them
    """
    qs_name = Contact.objects.values('name').annotate(dup_count=Count('name')).filter(
        dup_count__gt=1)  # name duplicates
    qs_email = Contact.objects.values('email').annotate(dup_count=Count('email')).filter(
        dup_count__gt=1)  # email duplicates
    qs_phones = Contact.objects.values('phone_numbers').annotate(dup_count=Count('phone_numbers')).filter(
        dup_count__gt=1
    )  # TODO: may have some bug =)
    merge_qs(qs_name)
    merge_qs(qs_email)
    merge_qs(qs_phones)
    logger.info("contacts merge successfully")
