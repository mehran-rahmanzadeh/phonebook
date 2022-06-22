import logging
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.validators import ValidationError as BasicValidationError
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from painless.otp.utils import otp_service
from authentication.api.serializers.auth_serializers import UsernamePasswordSerializer, UserOTPTokenSerializer
from painless.utils.constants.messages import (
    USER_NOT_FOUND,
    TOKEN_VALID,
    TOKEN_EXPIRED,
    YOU_CAN_NOT_RESET_PASSWORD,
    RESET_PASSWORD_SUCCESS,
    PASSWORD_NOT_VALID,
    ACCOUNT_NOT_ACTIVE,
    RESET_PASSWORD_FAILURE,
)
from painless.utils.serializers.serializers import PersianPhoneNumberSerializer

logger = logging.getLogger("root")
User = get_user_model()


class SendOTPResetPasswordView(APIView):
    serializer_class = PersianPhoneNumberSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        payload = request.data
        serializer = self.serializer_class(data=payload)
        if serializer.is_valid():
            phone_number = payload.get('phone_number')
            queryset = User.objects.filter(phone_number=phone_number)
            if not queryset.exists():
                message = USER_NOT_FOUND
                code = status.HTTP_404_NOT_FOUND
                return Response(
                    data={"message": message},
                    status=code
                )
            message, code = otp_service.send_token_to_user(phone_number)

        else:
            message = serializer.errors
            code = status.HTTP_400_BAD_REQUEST

        return Response(
            data={"message": message},
            status=code
        )


class OTPResetPasswordVerifyView(APIView):
    serializer_class = UserOTPTokenSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        payload = request.data
        serializer = self.serializer_class(data=payload)

        phone_number = payload.get('phone_number')
        token = payload.get('token')

        if serializer.is_valid():

            if otp_service.verify_token(token, phone_number):

                user = User.objects.filter(phone_number=phone_number)
                if user.exists():
                    message = TOKEN_VALID
                    code = status.HTTP_201_CREATED
                else:
                    message = USER_NOT_FOUND
                    code = status.HTTP_404_NOT_FOUND
            else:
                message = TOKEN_EXPIRED
                code = status.HTTP_403_FORBIDDEN
        else:
            message = serializer.errors
            code = status.HTTP_400_BAD_REQUEST

        return Response(
            data={"message": message},
            status=code
        )


class OTPResetPasswordView(APIView):
    serializer_class = UsernamePasswordSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        payload = request.data
        serializer = self.serializer_class(data=payload)

        phone_number = payload.get('phone_number')
        token = payload.get('token')

        if serializer.is_valid():
            if not otp_service.verify_token(token, phone_number):
                message = YOU_CAN_NOT_RESET_PASSWORD
                code = status.HTTP_403_FORBIDDEN
            else:
                user = User.objects.filter(phone_number=phone_number)
                if user.exists():
                    user = user.first()
                    if user.is_active:
                        try:
                            validate_password(payload.get("password"))
                            user.set_password(payload.get("password"))
                            user.save()
                            logger.info(f"{user} Reset Password Successfully")

                            response = {
                                'status': 'success',
                                'code': status.HTTP_200_OK,
                                'message': RESET_PASSWORD_SUCCESS,
                                'data': []
                            }

                            return Response(response)

                        except BasicValidationError as e:
                            return Response(
                                data={
                                    'message': PASSWORD_NOT_VALID,
                                    'data': e.messages,
                                },
                                status=status.HTTP_403_FORBIDDEN
                            )

                    else:
                        message = ACCOUNT_NOT_ACTIVE
                        code = status.HTTP_404_NOT_FOUND

                else:
                    message = USER_NOT_FOUND
                    code = status.HTTP_404_NOT_FOUND
        else:
            message = serializer.errors
            code = status.HTTP_400_BAD_REQUEST

        return Response(
            data={"message": message},
            status=code
        )
