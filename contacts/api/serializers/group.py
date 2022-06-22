from rest_framework.relations import SlugRelatedField
from rest_framework.serializers import ModelSerializer

from contacts.api.serializers.contact import ContactSerializer
from contacts.models.contact import Contact
from contacts.models.group import Group


class GroupSerializer(ModelSerializer):
    contacts = ContactSerializer(many=True)

    class Meta:
        model = Group
        fields = (
            'sku',
            'title',
            'contacts'
        )


class CreateGroupSerializer(ModelSerializer):
    contacts = SlugRelatedField(
        queryset=Contact.objects.all(),
        slug_field='sku',
        required=False
    )

    class Meta:
        model = Group
        fields = (
            'sku',
            'title',
            'contacts'
        )
        read_only_fields = ('sku',)
