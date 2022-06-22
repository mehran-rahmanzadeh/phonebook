import random
import logging
import redis
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from rest_framework import status

from painless.otp.services import iran_otp

logger = logging.getLogger("root")


class OtpService:

    def __init__(self):
        self.send_sms_message = ('send_sms_message',
                                 _("An sms is sent to your phone number. Please add sent code to text box."))

        self.redis_host = settings.OTP_REDIS_HOST
        self.redis_port = settings.OTP_REDIS_PORT
        self.redis_name = settings.OTP_REDIS_NAME
        self.redis = redis.Redis(self.redis_host, self.redis_port, self.redis_name)
        self.message = None
        self.code = None

    @staticmethod
    def generate_token():
        return str(random.randint(111111, 999999))

    def send_token_to_user(self, phone_number):
        token = self.generate_token()
        if settings.IS_GATE_ENABLED:
            message, send = iran_otp.send_token(to=phone_number, token=token)
            if send:
                logger.info(f"Token Sent To {phone_number}")
                self.insert_token_to_redis(token, phone_number)
                self.message = self.send_sms_message
                self.code = status.HTTP_201_CREATED
            else:
                logger.info(f"Send Token Failed To {phone_number}")
                self.message = 'Bad Request'
                self.code = status.HTTP_400_BAD_REQUEST
        else:
            self.insert_token_to_redis(token, phone_number)
            self.code = status.HTTP_201_CREATED
            self.message = f"token is {token}"

        return self.message, self.code

    def insert_token_to_redis(self, token, phone_number, expire_time=settings.OTP_TOKEN_EXPIRE_TIME):
        self.redis.setnx(token, phone_number)
        self.redis.expire(token, expire_time)

    def verify_token(self, code, phone_number):
        code_in_redis = self.redis.get(code)
        if code_in_redis is not None and str(code_in_redis, encoding="UTF8") == str(phone_number):
            logger.info(f"Remove {code} From Redis")
            self.redis.delete(code)
            return True
        else:
            return False


otp_service = OtpService()
