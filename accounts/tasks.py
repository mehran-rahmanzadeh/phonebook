from celery import shared_task
from celery.utils.log import get_task_logger

from painless.otp.services import iran_sms

logger = get_task_logger(__name__)


@shared_task
def send_sms_to_user(*args, **kwargs):
    phone_number = kwargs.get('phone_number')
    message = kwargs.get('message')
    message_, send = iran_sms.send_message(phone_number, message)
    logger.info(f'send message to {phone_number}: status {send} - {message_}')
