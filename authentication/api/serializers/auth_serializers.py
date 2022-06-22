from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.core.exceptions import ValidationError as DjangoValidationError


from painless.utils.serializers.serializers import (
    PersianPhoneNumberSerializer,
    PasswordSerializer,
    ResetPasswordSerializer,
    TokenSerializer,
)


class UsernamePasswordSerializer(PersianPhoneNumberSerializer, PasswordSerializer):
    pass


class ChangePasswordSerializer(ResetPasswordSerializer):
    pass


class UserOTPTokenSerializer(PersianPhoneNumberSerializer, TokenSerializer):
    pass


class PasswordChangeSerializer(serializers.Serializer):
    def __init__(self, user=None, *args, **kwargs):
        self.user = user
        super(PasswordChangeSerializer, self).__init__(*args, **kwargs)

    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_old_password(self, value):
        if self.user.check_password(value):
            return value
        else:
            raise ValidationError(
                detail={'message': 'Password is wrong'}
            )

    def validate_new_password(self, value):
        try:
            validate_password(value)
        except DjangoValidationError as e:
            raise ValidationError(
                detail={'message': e.messages}
            )
        return value


class TokenValidationSerializer(serializers.Serializer):
    uidb64 = serializers.CharField(required=True)
    token = serializers.CharField(required=True)


class PasswordResetConfirmSerializer(TokenValidationSerializer):
    new_password = serializers.CharField(required=True)

    def validate_new_password(self, value):
        try:
            validate_password(value)
        except DjangoValidationError as e:
            raise serializers.ValidationError(e.messages)
        return value
