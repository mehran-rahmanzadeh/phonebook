from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from painless.utils.constants.messages import (
    USER_EXISTS,
    USER_NOT_FOUND
)
from painless.utils.serializers.serializers import PersianPhoneNumberSerializer


class CheckUserExist(APIView):
    serializer_class = PersianPhoneNumberSerializer
    permission_classes = (AllowAny,)

    # throttle_classes = [AnonMembershipExistenceThrottle]

    def post(self, request, *args, **kwargs):
        payload = request.data
        serializer = self.serializer_class(data=payload)
        phone_number = payload.get('phone_number')

        if serializer.is_valid():
            user = get_user_model().objects.filter(phone_number=phone_number)
            if user.exists():
                message = USER_EXISTS
                code = status.HTTP_200_OK
            else:
                message = USER_NOT_FOUND
                code = status.HTTP_404_NOT_FOUND
        else:
            message = serializer.errors
            code = status.HTTP_400_BAD_REQUEST

        return Response(
            data={
                "message": message
            },
            status=code
        )
