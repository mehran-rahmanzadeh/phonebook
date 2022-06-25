from collections import ChainMap

from django.db.models import QuerySet
from django.forms import model_to_dict

from painless.utils.tools.dictionary import remove_none_values


def merge_qs(queryset: QuerySet):
    """merge qs objects to one primary object"""
    objs = [
        remove_none_values(model_to_dict(i, fields=['name', 'phone_numbers', 'email']) if not isinstance(i, dict) else i)
        for i in queryset.iterator()
    ]

    # merge all dictionaries
    merged_dict = ChainMap(*objs)

    # fetch merged data
    primary = queryset.first()
    print(primary)
    for k, v in merged_dict.items():
        if k == 'phone_numbers':
            primary.phone_numbers.set(v)
        else:
            setattr(primary, k, v)
    primary.save()

    # delete other records
    queryset.exclude(id=primary.id).delete()

    return primary
