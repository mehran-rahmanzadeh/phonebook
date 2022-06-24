from collections import ChainMap

from django.forms import model_to_dict
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from contacts.api.serializers.contact import (
    CreateContactSerializer,
    ContactSerializer,
    AddContactToGroupSerializer
)
from contacts.models.contact import Contact
from contacts.models.group import Group
from painless.utils.constants.messages import (
    ADDED_SUCCESS,
    REMOVED_SUCCESS,
    NO_DUPLICATE,
    NO_FILTER_TERM,
    MERGE_SUCCESS
)
from painless.utils.tools.dictionary import remove_none_values


class ContactViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ('name', 'phone_numbers__value', 'email')
    lookup_field = 'sku'

    def get_serializer_class(self):
        if self.action in ['create', 'update']:
            return CreateContactSerializer
        elif self.action in ['add_to_group', 'remove_from_group']:
            return AddContactToGroupSerializer
        return ContactSerializer

    def get_queryset(self):
        qs = Contact.objects.all()
        qs = qs.filter(user=self.request.user)
        return qs.prefetch_related('phone_numbers')

    @action(methods=['POST'], detail=True)
    def add_to_group(self, *args, **kwargs):
        payload = self.request.data
        serializer = self.get_serializer(data=payload)
        serializer.is_valid(raise_exception=True)
        group = get_object_or_404(Group, sku=payload.get('group'))
        instance = self.get_object()
        group.contacts.add(instance)
        response = {
            'message': ADDED_SUCCESS
        }
        code = status.HTTP_202_ACCEPTED
        return Response(data=response, status=code)

    @action(methods=['POST'], detail=True)
    def remove_from_group(self, *args, **kwargs):
        payload = self.request.data
        serializer = self.get_serializer(data=payload)
        serializer.is_valid(raise_exception=True)
        group = get_object_or_404(Group, sku=payload.get('group'))
        instance = self.get_object()
        group.contacts.remove(instance)
        response = {
            'message': REMOVED_SUCCESS
        }
        code = status.HTTP_202_ACCEPTED
        return Response(data=response, status=code)

    @action(methods=['GET'], detail=False)
    def duplicates(self, *args, **kwargs):
        merge = self.request.query_params.get('merge', False)
        qs = self.filter_queryset(self.get_queryset())

        # check is there duplicate values
        if qs.count() <= 1:
            response = {
                'message': NO_DUPLICATE
            }
            code = status.HTTP_204_NO_CONTENT
            return Response(data=response, status=code)

        # check filter query params provided by user
        if len(set(self.request.query_params.keys()).intersection(set(self.filterset_fields))) == 0:
            response = {
                'message': NO_FILTER_TERM
            }
            code = status.HTTP_400_BAD_REQUEST
            return Response(data=response, status=code)

        if merge:
            count = qs.count()
            # convert all objs to dict (using iterator for performance)
            objs = [
                remove_none_values(model_to_dict(i, fields=['name', 'phone_numbers', 'email']))
                for i in qs.iterator()
            ]

            # merge all dictionaries
            merged_dict = ChainMap(*objs)

            # fetch merged data
            primary = qs.first()
            for k, v in merged_dict.items():
                if k == 'phone_numbers':
                    primary.phone_numbers.set(v)
                else:
                    setattr(primary, k, v)
            primary.save()

            # delete other records
            qs.exclude(id=primary.id).delete()

            response = {
                'message': MERGE_SUCCESS.format(count)
            }
            code = status.HTTP_202_ACCEPTED
            return Response(data=response, status=code)

        page = self.paginate_queryset(qs)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(qs, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
