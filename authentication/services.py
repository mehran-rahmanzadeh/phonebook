import random

from django_redis import get_redis_connection
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.signing import Signer
from django.utils.crypto import get_random_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from painless.otp.services import iran_otp

User = get_user_model()


class Auth:
    chars = 'abcdefghijklmnopqrstuvwxyz0123456789'

    def __init__(self):
        self.redis_host = settings.OTP_REDIS_HOST
        self.redis_port = settings.OTP_REDIS_PORT
        self.redis_name = settings.OTP_REDIS_NAME
        self.redis = get_redis_connection('default')
        self.signer = Signer()

    @staticmethod
    def check_user_existence(phone_number):
        user_qs = User.objects.filter(phone_number=phone_number)
        return user_qs[0] if user_qs else None

    def generate_token(self, phone_number):
        token = get_random_string(30, self.chars)
        encrypted_token = self._save_token(token, str(phone_number))
        return encrypted_token

    @staticmethod
    def generate_otp():
        otp = random.randint(1000, 9999)
        return otp

    def generate_token_and_otp(self, phone_number):
        token = get_random_string(30, self.chars)
        otp = self.generate_otp()
        encrypted_token = self._save_token(token, phone_number)
        self.save_otp(phone_number, otp)
        return encrypted_token

    def _save_token(self, token, phone):
        self.redis.setex(token, 3600, phone)
        encrypted_token = self.encrypt_token(token)
        return encrypted_token

    def validate_token(self, token):
        if token:
            decrypted_token = self.decrypt_token(token)
            return bool(self.redis.exists(decrypted_token))
        return False

    def get_phone(self, token, encrypted=False):
        decrypted_token = self.decrypt_token(token)
        encrypted_phone = self.redis.get(decrypted_token)
        if encrypted:
            return encrypted_phone
        return self.decrypt_phone(encrypted_phone)

    def remove_token(self, token):
        decrypted_token = self.decrypt_token(token)
        self.redis.delete(decrypted_token)

    def save_otp(self, phone, otp):
        encrypted_phone = self.encrypt_phone(phone)
        encrypted_otp = self.signer.signature(otp)
        self.redis.setex(encrypted_phone, settings.OTP_EXPIRY_SECONDS, encrypted_otp)
        iran_otp.send_token(to=phone, token=otp)

    def validate_otp(self, phone, otp):
        try:
            otp = int(otp)
        except:
            return False
        if otp:
            encrypted_phone = self.encrypt_phone(phone)
            encrypted_otp_in_redis = self.redis.get(encrypted_phone)
            if encrypted_otp_in_redis and str(encrypted_otp_in_redis, encoding='utf-8') == self.signer.signature(otp):
                return True
        return False

    def remove_phone(self, phone):
        encrypted_phone = self.encrypt_phone(phone)
        self.redis.delete(encrypted_phone)

    def get_ttl(self, phone):
        encrypted_phone = self.encrypt_phone(phone)
        ttl = self.redis.ttl(encrypted_phone)
        return ttl if ttl >= 0 else 0

    def has_otp(self, token):
        phone = self.get_phone(token)
        encrypted_phone = self.encrypt_phone(phone)
        return True if self.redis.exists(encrypted_phone) else False

    @staticmethod
    def encrypt_token(token):
        encrypted_token = urlsafe_base64_encode(force_bytes(token))
        return encrypted_token

    @staticmethod
    def decrypt_token(token):
        decrypted_token = urlsafe_base64_decode(token).decode()
        return decrypted_token

    def encrypt_phone(self, phone):
        return self.signer.signature(phone)

    @staticmethod
    def decrypt_phone(phone):
        return phone
