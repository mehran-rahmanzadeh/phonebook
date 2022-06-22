import logging
from painless.otp.utils import otp_service
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from authentication.api.serializers.auth_serializers import UserOTPTokenSerializer, UsernamePasswordSerializer
from painless.utils.constants.messages import (
    USER_EXISTS,
    TOKEN_EXPIRED,
    TOKEN_VALID,
    REGISTER_SUCCESS,
)
from painless.utils.serializers.serializers import PersianPhoneNumberSerializer

logger = logging.getLogger("root")

User = get_user_model()


class SendOTPRegisterView(APIView):
    serializer_class = PersianPhoneNumberSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        payload = request.data
        serializer = self.serializer_class(data=payload)
        phone_number = payload.get('phone_number')

        queryset = User.objects.filter(phone_number=payload.get('phone_number'))
        if queryset.exists():
            message = USER_EXISTS
            code = status.HTTP_409_CONFLICT
            return Response(
                data={"message": message},
                status=code
            )

        if serializer.is_valid():
            message, code = otp_service.send_token_to_user(phone_number)
        else:
            message = serializer.errors
            code = status.HTTP_400_BAD_REQUEST

        logger.info(message)
        return Response(
            data={"message": message},
            status=code
        )


class OTPRegisterVerifyView(APIView):
    serializer_class = UserOTPTokenSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        payload = request.data
        phone_number = payload.get('phone_number')
        token = payload.get('token')
        serializer = self.serializer_class(data=payload)

        user = User.objects.filter(phone_number=phone_number)
        if user.exists():
            message = USER_EXISTS
            code = status.HTTP_200_OK
            logger.info(message)
            return Response(
                data={
                    'message': message
                },
                status=code
            )

        if serializer.is_valid():
            if otp_service.verify_token(token, phone_number):
                message = TOKEN_VALID
                code = status.HTTP_201_CREATED
            else:
                message = TOKEN_EXPIRED
                code = status.HTTP_403_FORBIDDEN
        else:
            message = serializer.errors
            code = status.HTTP_400_BAD_REQUEST

        logger.info(message)
        return Response(
            data={
                'message': message
            },
            status=code
        )


class UserRegisterView(APIView):
    serializer_class = UsernamePasswordSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        payload = request.data
        serializer = self.serializer_class(data=payload)

        phone_number = payload.get('phone_number')
        password = payload.get('password')

        user = get_user_model().objects.filter(phone_number=phone_number)
        if user.exists():
            message = USER_EXISTS
            code = status.HTTP_200_OK
            logger.info(message)
            return Response(
                data={
                    'message': message
                },
                status=code
            )

        if serializer.is_valid():
            user = User.objects.create_user(
                phone_number=phone_number,
                password=password
            )
            user.is_active = True
            user.is_phone_confirmed = True
            user.save()
            message = REGISTER_SUCCESS
            code = status.HTTP_201_CREATED
        else:
            message = serializer.errors
            code = status.HTTP_400_BAD_REQUEST

        logger.info(message)
        return Response(
            data={
                "message": message
            },
            status=code
        )
