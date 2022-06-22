from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from accounts.api.serializers.user import UserSerializer

User = get_user_model()


class UserViewSet(ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'sku'

    def get_queryset(self):
        qs = super(UserViewSet, self).get_queryset()
        return qs.filter(sku=self.request.user.sku)
