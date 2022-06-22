from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
import logging
from authentication.api.serializers.auth_serializers import PasswordChangeSerializer

logger = logging.getLogger("root")


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        serializer = PasswordChangeSerializer(data=request.data, user=user)
        serializer.is_valid(raise_exception=True)
        new_password = serializer.validated_data['new_password']
        request.user.set_password(new_password)
        logger.info(f"{user} Changed Password Successfully")
        request.user.save()
        return Response(data={'message': 'Password successfully changed'})
