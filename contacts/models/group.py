import secrets

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _

from contacts.models.contact import Contact
from painless.utils.models.mixins import Sku_Mixin, TimeStampModelMixin


class Group(Sku_Mixin, TimeStampModelMixin):
    title = models.CharField(
        _('Title'),
        max_length=100
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='contact_groups',
        verbose_name=_('Group'),
        on_delete=models.CASCADE
    )

    contacts = models.ManyToManyField(
        Contact,
        verbose_name=_('Contacts'),
        related_name='contact_groups',
        blank=True
    )

    def __str__(self):
        return f'contact group {self.sku} of user {self.user.sku}'

    def save(self, *args, **kwargs):
        if not self.sku:
            self.sku = secrets.token_urlsafe(12)
        super(Group, self).save(*args, **kwargs)
