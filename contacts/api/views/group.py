from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from contacts.api.serializers.group import (
    CreateGroupSerializer,
    GroupSerializer
)


class GroupViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    lookup_field = 'sku'

    def get_serializer_class(self):
        if self.action in ['create', 'update']:
            return CreateGroupSerializer
        return GroupSerializer

    def get_queryset(self):
        qs = super(GroupViewSet, self).get_queryset()
        return qs.filter(user=self.request.user)
