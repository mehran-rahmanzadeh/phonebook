from django.contrib import admin

from contacts.models.contact import Contact
from contacts.models.group import Group
from contacts.models.phone_number import PhoneNumber


@admin.register(PhoneNumber)
class PhoneNumberModelAdmin(admin.ModelAdmin):
    pass


@admin.register(Contact)
class ContactModelAdmin(admin.ModelAdmin):
    pass


@admin.register(Group)
class GroupModelAdmin(admin.ModelAdmin):
    pass
