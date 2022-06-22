from django.conf import settings

from django.db import models

from django.conf import settings

from django.core.validators import (
    MaxLengthValidator,
    MinLengthValidator,
    FileExtensionValidator
)
from safedelete import SOFT_DELETE_CASCADE
from safedelete.models import SafeDeleteModel

from painless.utils.upload.path import (
    date_directory_path,
    user_directory_path
)

from django.utils.translation import ugettext_lazy as _


class Sku_Mixin(models.Model):
    sku = models.CharField(
        max_length=255,
        editable=False,
        unique=True,
        db_index=True,
        null=True,
        default=None
    )

    class Meta:
        abstract = True


class TitleSlugLinkModelMixin(models.Model):
    title = models.CharField(
        _("Title"),
        max_length=150,
        validators=[
            MaxLengthValidator(150),
            MinLengthValidator(3)
        ],
        unique=True
    )
    slug = models.SlugField(
        _("Slug"),
        editable=False,
        allow_unicode=True,
        max_length=150,
        unique=True
    )

    class Meta:
        abstract = True


class TimeStampModelMixin(models.Model):
    created = models.DateTimeField(
        _("Created"),
        auto_now_add=True
    )
    modified = models.DateTimeField(
        _("Modified"),
        auto_now=True
    )

    class Meta:
        abstract = True


class DeletedAtMixin(models.Model):
    deleted_at = models.DateTimeField(
        null=True,
        blank=True
    )

    class Meta:
        abstract = True


class SVGMixin(models.Model):
    svg = models.FileField(
        _("SVG"),
        upload_to=date_directory_path,
        max_length=110,
        validators=[FileExtensionValidator(allowed_extensions=['svg', 'SVG'])]
    )

    svg_alternate_text = models.CharField(
        _("Alternate Text"),
        max_length=110,
        validators=[
            MaxLengthValidator(150),
            MinLengthValidator(3)
        ]
    )

    class Meta:
        abstract = True


class WightSVGMixin(models.Model):
    wight_svg = models.FileField(
        _("Wight SVG"),
        upload_to=date_directory_path,
        max_length=110,
        validators=[FileExtensionValidator(allowed_extensions=['svg', 'SVG'])]
    )

    wight_svg_alternate_text = models.CharField(
        _("Wight Svg Alternate Text"),
        max_length=110,
        validators=[
            MaxLengthValidator(150),
            MinLengthValidator(3)
        ]
    )

    class Meta:
        abstract = True


class ImageMixin(models.Model):
    picture = models.ImageField(
        _("Picture"),
        upload_to=date_directory_path,
        height_field='height_field',
        width_field='width_field',
        max_length=110,
        validators=[FileExtensionValidator(
            allowed_extensions=['JPG', 'JPEG', 'PNG', 'jpg', 'jpeg', 'png'])]
    )

    alternate_text = models.CharField(
        _("Alternate Text"),
        max_length=110,
        validators=[
            MaxLengthValidator(150),
            MinLengthValidator(3)
        ]
    )
    width_field = models.PositiveSmallIntegerField(
        _("Width Field"),
        editable=False
    )
    height_field = models.PositiveSmallIntegerField(
        _("Height Field"),
        editable=False
    )

    class Meta:
        abstract = True


class ImageNullableMixin(models.Model):
    picture = models.ImageField(
        _("Picture"),
        upload_to=date_directory_path,
        height_field='height_field',
        width_field='width_field',
        max_length=110,
        validators=[FileExtensionValidator(
            allowed_extensions=['JPG', 'JPEG', 'PNG', 'jpg', 'jpeg', 'png'])],
        null=True,
        blank=True
    )

    alternate_text = models.CharField(
        _("Alternate Text"),
        max_length=110,
        validators=[
            MaxLengthValidator(150),
            MinLengthValidator(3)
        ],
        null=True,
        blank=True
    )
    width_field = models.PositiveSmallIntegerField(
        _("Width Field"),
        editable=False,
        null=True,
        blank=True
    )
    height_field = models.PositiveSmallIntegerField(
        _("Height Field"),
        editable=False,
        null=True,
        blank=True
    )

    class Meta:
        abstract = True


class ImagePNG_Mixin(models.Model):
    picture = models.ImageField(
        _("Picture"),
        upload_to=date_directory_path,
        height_field='height_field',
        width_field='width_field',
        max_length=110,
        validators=[FileExtensionValidator(allowed_extensions=['PNG', 'png'])]
    )

    alternate_text = models.CharField(
        _("Alternate Text"),
        max_length=110,
        validators=[
            MaxLengthValidator(150),
            MinLengthValidator(3)
        ]
    )
    width_field = models.PositiveSmallIntegerField(
        _("Width Field"),
        editable=False
    )
    height_field = models.PositiveSmallIntegerField(
        _("Height Field"),
        editable=False
    )

    class Meta:
        abstract = True


class ImageJPG_Mixin(models.Model):
    picture = models.ImageField(
        _("Picture"),
        upload_to=date_directory_path,
        height_field='height_field',
        width_field='width_field',
        max_length=110,
        validators=[FileExtensionValidator(allowed_extensions=['JPG', 'JPEG', 'jpg', 'jpeg'])]
    )

    alternate_text = models.CharField(
        _("Alternate Text"),
        max_length=110,
        validators=[
            MaxLengthValidator(150),
            MinLengthValidator(3)
        ]
    )
    width_field = models.PositiveSmallIntegerField(
        _("Width Field"),
        editable=False
    )
    height_field = models.PositiveSmallIntegerField(
        _("Height Field"),
        editable=False
    )

    class Meta:
        abstract = True


class PremiumMixin(models.Model):
    METHODS = (
        ('f', _('Freemium')),
        ('Z', _('Zarin')),
    )

    payment_method = models.CharField(
        _("Payment Method"),
        choices=METHODS,
        max_length=1,
        default='f'
    )

    class Meta:
        abstract = True


class LevelMixin(models.Model):
    LEVELS = (
        ('b', _('Basic')),
        ('i', _('Intermediate')),
        ('a', _('Advance')),
        ('p', _('Professional')),
    )

    level = models.CharField(
        _("Level"),
        choices=LEVELS,
        max_length=1,
        default='b'
    )

    class Meta:
        abstract = True


class CoverMixin(models.Model):
    cover = models.ImageField(
        _("Cover"),
        upload_to=date_directory_path,
        height_field='cover_height_field',
        width_field='cover_width_field',
        max_length=110,
        validators=[FileExtensionValidator(
            allowed_extensions=['JPG', 'JPEG', 'PNG', 'jpg', 'jpeg', 'png'])]
    )

    cover_alternate_text = models.CharField(
        _("Alternate Text"),
        max_length=110,
        validators=[
            MaxLengthValidator(150),
            MinLengthValidator(3)
        ]
    )
    cover_width_field = models.PositiveSmallIntegerField(
        _("Width Field"),
        editable=False
    )
    cover_height_field = models.PositiveSmallIntegerField(
        _("Height Field"),
        editable=False
    )

    class Meta:
        abstract = True


class PDFModelMixin(models.Model):
    pdf = models.FileField(
        _("Pdf File"),
        upload_to=date_directory_path,
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'PDF'])],
        null=True,
        blank=True
    )

    class Meta:
        abstract = True


class SafeDeleteModelMixin(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE

    class Meta:
        abstract = True
