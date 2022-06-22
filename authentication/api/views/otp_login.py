from django.contrib.auth import get_user_model
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
import logging
from authentication.api.serializers.auth_serializers import UserOTPTokenSerializer
from painless.otp.utils import otp_service
from painless.utils.constants.messages import (
    USER_NOT_FOUND,
    LOGIN_SUCCESS,
    ACCOUNT_NOT_ACTIVE,
    LOGIN_FAILURE,
)
from painless.utils.serializers.serializers import PersianPhoneNumberSerializer

User = get_user_model()
logger = logging.getLogger("root")


class SendOTPLoginView(APIView):
    serializer_class = PersianPhoneNumberSerializer
    permission_classes = (AllowAny,)

    @swagger_auto_schema(responses={status.HTTP_201_CREATED: PersianPhoneNumberSerializer()},
                         request_body=PersianPhoneNumberSerializer)
    def post(self, request, *args, **kwargs):
        payload = request.data
        serializer = self.serializer_class(data=payload)
        phone_number = payload.get('phone_number')

        if serializer.is_valid():
            user = User.objects.filter(phone_number=phone_number)
            if user.exists():
                message, code = otp_service.send_token_to_user(phone_number)
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


class OTPLoginView(APIView):
    serializer_class = UserOTPTokenSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        payload = request.data
        serializer = self.serializer_class(data=payload)

        phone_number = payload.get('phone_number')
        token = payload.get('token')

        if serializer.is_valid():

            user = User.objects.filter(phone_number=phone_number)
            if user.exists():
                user = user.first()
                if otp_service.verify_token(token, phone_number):
                    if user.is_active:
                        refresh = RefreshToken.for_user(user)
                        logger.info(f"{user} logged in successfully")
                        return Response(
                            data={
                                'message': LOGIN_SUCCESS,
                                'data': {
                                    'refresh': str(refresh),
                                    'access': str(refresh.access_token),
                                }
                            },
                            status=status.HTTP_200_OK
                        )

                    else:
                        message = ACCOUNT_NOT_ACTIVE
                        code = status.HTTP_404_NOT_FOUND

                else:
                    message = LOGIN_FAILURE
                    code = status.HTTP_400_BAD_REQUEST

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
