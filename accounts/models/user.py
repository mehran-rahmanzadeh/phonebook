import logging
import secrets
import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy as _

from accounts.managers import CustomUserManager, ActiveUserManager
from painless.utils.models.mixins import Sku_Mixin, TimeStampModelMixin
from painless.utils.models.validations import PersianPhoneNumberValidator

logger = logging.getLogger("root")


class CustomUser(Sku_Mixin, AbstractUser, TimeStampModelMixin):
    username = None
    phone_number = models.CharField(
        _('phone number'),
        unique=True,
        max_length=15,
        validators=[PersianPhoneNumberValidator],
        error_messages={
            'unique': _("A user with that phone number already exists."),
        },
    )
    secret = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        help_text='توکنی برای ارسال تاییده ایمیل'
    )
    is_phone_confirmed = models.BooleanField(
        _('Is phone confirmed'),
        default=False
    )
    last_day_contact_count = models.PositiveBigIntegerField(
        _('Last day contact count'),
        default=0
    )

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()
    actives = ActiveUserManager()

    def __str__(self):
        return f'{self.get_full_name()}-{self.phone_number}'

    def save(self, *args, **kwargs):
        if not self.sku:
            self.sku = secrets.token_urlsafe(16)
            logger.info(f'user register {self.sku}')
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
