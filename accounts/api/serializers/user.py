from django.contrib.auth import get_user_model
from rest_framework.serializers import ModelSerializer

User = get_user_model()


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = (
            'sku',
            'phone_number',
            'first_name',
            'last_name',
            'is_phone_confirmed',
            'date_joined'
        )
        read_only_fields = (
            'sku',
            'is_phone_confirmed',
            'phone_number',
            'date_joined'
        )
