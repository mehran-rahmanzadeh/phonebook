import secrets

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _

from contacts.models.phone_number import PhoneNumber
from painless.utils.models.mixins import Sku_Mixin, TimeStampModelMixin


class Contact(Sku_Mixin, TimeStampModelMixin):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('User'),
        related_name='contacts',
        on_delete=models.CASCADE
    )

    name = models.CharField(
        _('Name'),
        max_length=50
    )

    phone_numbers = models.ManyToManyField(
        PhoneNumber,
        verbose_name=_('Phone Numbers'),
        related_name='contacts',
        blank=True
    )

    email = models.EmailField(
        verbose_name=_('Email'),
        blank=True,
        null=True
    )

    def __str__(self):
        return f'contact {self.sku} of user {self.user}'

    def save(self, *args, **kwargs):
        if not self.sku:
            self.sku = secrets.token_urlsafe(12)
        super(Contact, self).save(*args, **kwargs)
