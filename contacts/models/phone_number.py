import secrets

from django.db import models
from django.utils.translation import ugettext_lazy as _

from painless.utils.models.mixins import Sku_Mixin, TimeStampModelMixin
from painless.utils.models.validations import PersianPhoneNumberValidator


class PhoneNumber(Sku_Mixin, TimeStampModelMixin):
    value = models.CharField(
        _('Value'),
        max_length=15,
        validators=[PersianPhoneNumberValidator],
        unique=True
    )

    def __str__(self):
        return f'phone number: {self.value}'

    def save(self, *args, **kwargs):
        if not self.sku:
            self.sku = secrets.token_urlsafe(12)
        super(PhoneNumber, self).save(*args, **kwargs)
