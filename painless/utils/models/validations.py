import re

from django.core.exceptions import ValidationError
from django.core.files.images import get_image_dimensions
from django.core.validators import (
    RegexValidator
)
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _

from painless.utils.regex.patterns import PERSIAN_PHONE_NUMBER_PATTERN


@deconstructible
class NameValidator:
    def __init__(self, message=None):
        self.message = message

    def __call__(self, value):
        if re.search(r'\d', value):
            raise ValidationError(message=self.message or _('Enter a valid name'))

    def __eq__(self, other):
        return (
                isinstance(other, self.__class__) and
                self.allowed_extensions == other.allowed_extensions and
                self.message == other.message and
                self.code == other.code
        )


@deconstructible
class PersianPhoneNumberValidator(RegexValidator):
    regex = PERSIAN_PHONE_NUMBER_PATTERN
    message = _(
        'Enter a valid phone number'
    )
    flags = 0


@deconstructible
class PersianPostalCodeValidator(RegexValidator):
    regex = '^[0-9]{10}$',
    message = _('Enter a valid postal code')


@deconstructible
class DimensionValidator(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def __call__(self, value):
        pic = value
        w, h = get_image_dimensions(pic)

        if not (w == self.width and h == self.height):
            raise ValidationError(
                _('Expected Dim: [ %(width)sw , %(height)sh ] But Actual Dim: [ %(w)sw , %(h)sh ].'),
                params={"width": self.width, "height": self.height, "w": w, "h": h}
            )


@deconstructible
class SquareDimension(object):
    def __init__(self, *args, **kwargs):
        pass

    def __call__(self, value):
        pic = value
        w, h = get_image_dimensions(pic)

        if not (w == h):
            raise ValidationError(
                _('Width and Height must be equal (square image).')
            )


def validate_comma_seperator(value):
    if ',' not in value:
        raise ValidationError(
            _('%(value)s is not a comma-separated list.'),
            params={"value": value}
        )


def validate_placeholder(value):
    if '(---)' in value:
        raise ValidationError(
            _('%(value)s is not placeholder format.'),
            params={"value": value}
        )


def validate_(value):
    if '(---)' in value:
        raise ValidationError(
            _('%(value)s is not placeholder format.'),
            params={"value": value}
        )
