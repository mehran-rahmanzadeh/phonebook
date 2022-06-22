import secrets
import uuid
from django.db import models

from .mixins import (
    Sku_Mixin,
    TitleSlugLinkModelMixin,
    TimeStampModelMixin,
    DeletedAtMixin
)


class UUIDBaseModel(models.Model):
    sku = models.UUIDField(
        primary_key=False,
        default=uuid.uuid4,
        editable=False,
        unique=True,
        db_index=True
    )

    class Meta:
        abstract = True


class TraditionalBaseModel(Sku_Mixin, TitleSlugLinkModelMixin, TimeStampModelMixin, DeletedAtMixin):
    class Meta:
        abstract = True


class AutoSku(Sku_Mixin):
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.sku:
            self.sku = secrets.token_urlsafe(16)
        super().save(*args, **kwargs)
