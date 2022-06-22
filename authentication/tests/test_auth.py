import redis
from django.conf import settings
from django.contrib.auth import get_user_model, authenticate
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework_simplejwt.tokens import RefreshToken

from authentication.tests.services import generate_token, insert_token_to_redis

User = get_user_model()


class TestAuth(APITestCase):
    def setUp(self) -> None:
        self.admin = User.objects.create_user(
            phone_number='09366408221',
            password='1234',
            is_superuser=True
        )
        self.admin.save()

    def test_username_password_login_success(self):
        data = {
            'phone_number': '09366408221',
            'password': '1234'
        }
        url = reverse('token_obtain_pair')
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data.get('refresh'))
        self.assertTrue(response.data.get('access'))

    def test_refresh_token_success(self):
        refresh = RefreshToken.for_user(self.admin)
        data = {
            'refresh': str(refresh)
        }
        url = reverse('token_refresh')
        response = self.client.post(url, data)
        self.assertIn('access', response.data)

    def test_authorized_change_password_success(self):
        refresh = RefreshToken.for_user(self.admin)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        data = {
            "old_password": "1234",
            "new_password": "09366408221f"
        }
        url = reverse('change-password')
        response = self.client.post(url, data)
        user_authenticated = authenticate(username=self.admin.phone_number, password='09366408221f')
        user_unauthorized = authenticate(username=self.admin.phone_number, password='1234')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(user_authenticated)
        self.assertFalse(user_unauthorized)

    def test_unauthorized_change_password_fail(self):
        self.client.logout()
        data = {
            "old_password": "1234",
            "new_password": "09366408221f"
        }
        url = reverse('change-password')
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 401)

    def test_otp_login_send_token_success(self):
        url = reverse('send-otp-login')
        data = {
            "phone_number": "09366408221"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)

    def test_otp_login_enter_code_success(self):
        token = generate_token()
        insert_token_to_redis(token, '09366408221')
        url = reverse('validate-otp-login')
        data = {
            'phone_number': '09366408221',
            'token': token
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('access', response.data.get('data'))
        self.assertIn('refresh', response.data.get('data'))

    def test_redis_remove_otp_after_login_success(self):
        token = generate_token()
        redis_host = settings.OTP_REDIS_HOST
        redis_port = settings.OTP_REDIS_PORT
        redis_name = settings.OTP_REDIS_NAME
        expire_time = settings.OTP_TOKEN_EXPIRE_TIME
        rd = redis.Redis(redis_host, redis_port, redis_name)
        rd.setnx(token, '09366408221')
        rd.expire(token, expire_time)
        token_before_login = rd.get(token)
        self.assertEqual(token_before_login, b'09366408221')
        url = reverse('validate-otp-login')
        data = {
            'phone_number': '09366408221',
            'token': token
        }
        self.client.post(url, data)
        token_after_login = rd.get(token)
        self.assertIsNone(token_after_login)

    def test_can_get_token_for_login_if_not_auth_fail(self):
        """
        Not registered user can't send token request
        """
        data = {
            'phone_number': '09999999999'
        }
        response = self.client.post(reverse('send-otp-login'), data)
        self.assertEqual(response.status_code, 404)

    def test_otp_login_verify_token_fail(self):
        data = {
            'phone_number': '09366408221',
            'token': '111111'
        }
        response = self.client.post(reverse('validate-otp-login'), data)
        self.assertEqual(response.status_code, 400)

    def test_user_existence_success(self):
        """
        Existing user
        """
        data = {
            'phone_number': self.username
        }
        response = self.client.post(reverse('check-user-existence'), data=data)
        self.assertEqual(response.status_code, 200)

    def test_user_existence_fail(self):
        """
        Not existing user
        """
        data = {
            'phone_number': '09999999999'
        }
        response = self.client.post(reverse('check-user-existence'), data=data)
        self.assertEqual(response.status_code, 404)
