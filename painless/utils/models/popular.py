import uuid

from django.conf import settings
from django.core.validators import FileExtensionValidator, MaxLengthValidator, MinLengthValidator
from django.db import models
from django.utils.translation import ugettext_lazy as _

from painless.utils.models.mixins import Sku_Mixin
from painless.utils.upload.path import user_directory_path


class UUIDBaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)

    class Meta:
        abstract = True


class TimeStampModelMixin(models.Model):
    created = models.DateTimeField(_("Created"), auto_now_add=True)
    modified = models.DateTimeField(_("Modified"), auto_now=True)

    class Meta:
        abstract = True


class UserImageUpload(Sku_Mixin, TimeStampModelMixin):
    image = models.ImageField(
        _("Avatar"),
        upload_to=user_directory_path,
        height_field='height_field',
        width_field='width_field',
        max_length=110,
        null=True, blank=True,
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])]
    )
    width_field = models.PositiveSmallIntegerField(_("Width Field"), null=True, blank=True, editable=False)
    height_field = models.PositiveSmallIntegerField(_("Height Field"), null=True, blank=True, editable=False)

    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("User"), related_name='images',
                             on_delete=models.CASCADE)

    object_id = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        abstract = True


class UserImageAltUpload(UUIDBaseModel, TimeStampModelMixin):
    image = models.ImageField(
        _("Avatar"),
        upload_to=user_directory_path,
        height_field='height_field',
        width_field='width_field',
        max_length=110,
        validators=[FileExtensionValidator(allowed_extensions=['JPG', 'JPEG', 'PNG', 'jpg', 'jpeg', 'png'])]
    )

    alternate_text = models.CharField(
        _("Alternate Text"),
        max_length=110,
        validators=[
            MaxLengthValidator(150),
            MinLengthValidator(3)
        ]
    )
    width_field = models.PositiveSmallIntegerField(_("Width Field"), null=True, blank=True, editable=False)
    height_field = models.PositiveSmallIntegerField(_("Height Field"), null=True, blank=True, editable=False)

    SCOPES = (
        ('user', _('User')),
        ('service', _('service')),
        ('category', _('category')),
    )

    object_scope = models.CharField(max_length=10, choices=SCOPES, null=True, blank=True)

    user = models.ForeignKey("User", verbose_name=_("User"), related_name='images', on_delete=models.CASCADE)

    class Meta:
        abstract = True
