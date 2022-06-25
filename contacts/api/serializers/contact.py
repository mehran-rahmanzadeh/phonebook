from django.core.exceptions import ObjectDoesNotExist
from django.utils.encoding import smart_text
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from contacts.api.serializers.phone_number import PhoneNumberSerializer
from contacts.models.contact import Contact
from contacts.models.phone_number import PhoneNumber


class GetOrCreateSlugRelatedField(serializers.SlugRelatedField):

    def to_internal_value(self, data):
        try:
            return self.get_queryset().get_or_create(**{self.slug_field: data})[0]
        except ObjectDoesNotExist:
            self.fail('does_not_exist', slug_name=self.slug_field, value=smart_text(data))
        except (TypeError, ValueError):
            self.fail('invalid')


class ContactSerializer(ModelSerializer):
    """Contact serializer"""
    phone_numbers = PhoneNumberSerializer(many=True)

    class Meta:
        model = Contact
        fields = (
            'sku',
            'name',
            'phone_numbers',
            'email',
            'created',
            'modified'
        )


class CreateContactSerializer(ModelSerializer):
    """Create contact serializer
    phone_numbers: [
        "0904714710",
        "080198410"
    ]
    """
    phone_numbers = GetOrCreateSlugRelatedField(
        queryset=PhoneNumber.objects.all(),
        slug_field='value',
        required=False,
        many=True
    )
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Contact
        fields = (
            'name',
            'phone_numbers',
            'email',
            'user'
        )


class AddContactToGroupSerializer(serializers.Serializer):
    """Add contact to group serializer"""
    group = serializers.CharField(required=True)
