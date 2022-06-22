from celery import shared_task
from celery.utils.log import get_task_logger

from painless.otp.services import iran_otp

logger = get_task_logger(__name__)


@shared_task
def send_otp(*args, **kwargs):
    phone_number = kwargs['phone_number']
    token = kwargs['token']
    message, send = iran_otp.send_token(phone_number, token)
    logger.info(f'sent:{send}-phone number: {phone_number}')
