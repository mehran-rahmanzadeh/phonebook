from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)

from .views.change_password import ChangePasswordView
from .views.otp_login import SendOTPLoginView, OTPLoginView
from .views.otp_register import (
    SendOTPRegisterView,
    OTPRegisterVerifyView,
    UserRegisterView
)
from .views.otp_reset_password import (
    SendOTPResetPasswordView,
    OTPResetPasswordView,
    OTPResetPasswordVerifyView,
)
from .views.user_existence import CheckUserExist

urlpatterns = [
    # Change password
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    # Login OTP
    path('login/otp/', SendOTPLoginView.as_view(), name='send-otp-login'),
    path('login/otp/validation/', OTPLoginView.as_view(), name='validate-otp-login'),
    # Reset password OTP
    path('reset-password/otp/', SendOTPResetPasswordView.as_view(), name='send-otp-reset-password'),
    path('reset-password/otp/validation/', OTPResetPasswordVerifyView.as_view(), name='validate-otp-reset-password'),
    path('reset-password/', OTPResetPasswordView.as_view(), name='reset-password'),
    # Check user existence
    path('membership/', CheckUserExist.as_view(), name='check-user-existence'),
    # Register OTP
    path('registration/otp/', SendOTPRegisterView.as_view(), name='send-register-otp'),
    path('registration/otp/validation/', OTPRegisterVerifyView.as_view(), name='validate-otp-register'),
    path('registration/', UserRegisterView.as_view(), name='user-register'),
    # JWT
    path('token/create/', TokenObtainPairView.as_view(), name='token-obtain-pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
]

