from rest_framework.serializers import ModelSerializer

from contacts.models.phone_number import PhoneNumber


class PhoneNumberSerializer(ModelSerializer):
    class Meta:
        model = PhoneNumber
        fields = (
            'value',
        )
