import random
import redis
from django.conf import settings


def generate_token():
    return str(random.randint(111111, 999999))


def insert_token_to_redis(token, phone_number, expire_time=settings.OTP_TOKEN_EXPIRE_TIME):
    redis_host = settings.OTP_REDIS_HOST
    redis_port = settings.OTP_REDIS_PORT
    redis_name = settings.OTP_REDIS_NAME
    rd = redis.Redis(redis_host, redis_port, redis_name)
    rd.setnx(token, phone_number)
    rd.expire(token, expire_time)
