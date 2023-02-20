import re
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _

from django.contrib.auth.password_validation import UserAttributeSimilarityValidator
from django.contrib.auth.password_validation import (
    CommonPasswordValidator,
    NumericPasswordValidator
)
from django.utils.translation import gettext as _, ngettext
import re
from difflib import SequenceMatcher

from django.core.exceptions import (
    FieldDoesNotExist, ValidationError,
)
from django.utils.translation import gettext as _, ngettext


def exceeds_maximum_length_ratio(password, max_similarity, value):
    """
    Test that value is within a reasonable range of password.

    The following ratio calculations are based on testing SequenceMatcher like
    this:

    for i in range(0,6):
      print(10**i, SequenceMatcher(a='A', b='A'*(10**i)).quick_ratio())

    which yields:

    1 1.0
    10 0.18181818181818182
    100 0.019801980198019802
    1000 0.001998001998001998
    10000 0.00019998000199980003
    100000 1.999980000199998e-05

    This means a length_ratio of 10 should never yield a similarity higher than
    0.2, for 100 this is down to 0.02 and for 1000 it is 0.002. This can be
    calculated via 2 / length_ratio. As a result we avoid the potentially
    expensive sequence matching.
    """
    pwd_len = len(password)
    length_bound_similarity = max_similarity / 2 * pwd_len
    value_len = len(value)
    return pwd_len >= 10 * value_len and value_len < length_bound_similarity


class UppercaseValidator(object):
    def validate(self, password, user=None):
        if not re.findall('[A-Z]', password):
            raise ValidationError(
                _("Şifrədə ən azı 1 böyük hərf olmalıdır, A-Z."),
                code='password_no_upper',
            )

    def get_help_text(self):
        return _(
            "Şifrənizdə ən azı 1 böyük hərf olmalıdır, A-Z."
        )

class SymbolValidator(object):
    def validate(self, password, user=None):
        if not re.findall('[()[\]{}|\\`~!@#$%^&*_\-+=;:\'",<>./?]', password):
            raise ValidationError(
                _("Şifrədə ən azı 1 simvol olmalıdır: " +
                  "()[]{}|\`~!@#$%^&*_-+=;:'\",<>./?"),
                code='password_no_symbol',
            )

    def get_help_text(self):
        return _(
            "Şifrənizdə ən azı 1 simvol olmalıdır: " +
            "()[]{}|\`~!@#$%^&*_-+=;:'\",<>./?"
        )

class NumberValidator(NumericPasswordValidator):
    def validate(self, password, user=None):
        if password.isdigit():
            raise ValidationError(
                _("Bu şifrə tamamilə rəqəmlidir."),
                code='password_entirely_numeric',
            )

    def get_help_text(self):
        return _('Şifrəniz tamamilə rəqəm ola bilməz.')

class MinimumLengthValidator(object):
    """
    Validate whether the password is of a minimum length.
    """
    def __init__(self, min_length=8):
        self.min_length = min_length

    def validate(self, password, user=None):
        if len(password) < self.min_length:
            raise ValidationError(
                ngettext(
                    "Bu şifrə çox qısadır. O, ən azı %(min_length)d simvoldan ibarət olmalıdır.",
                    "Bu şifrə çox qısadır. O, ən azı %(min_length)d simvoldan ibarət olmalıdır.",
                    self.min_length
                ),
                code='password_too_short',
                params={'min_length': self.min_length},
            )

    def get_help_text(self):
        return ngettext(
            "Şifrəniz ən azı %(min_length)d simvoldan ibarət olmalıdır.",
            "Şifrəniz ən azı %(min_length)d simvoldan ibarət olmalıdır.",
            self.min_length
        ) % {'min_length': self.min_length}

class CustomUserAttributeSimilarityValidator(UserAttributeSimilarityValidator):
    DEFAULT_USER_ATTRIBUTES = ('username', 'fullname')

    def __init__(self, user_attributes=DEFAULT_USER_ATTRIBUTES, max_similarity=0.7):
        self.user_attributes = user_attributes
        if max_similarity < 0.1:
            raise ValueError('maksimum oxşarlıq ən azı 0,1 olmalıdır')
        self.max_similarity = max_similarity

    def validate(self, password, user=None):
        if not user:
            return

        password = password.lower()
        for attribute_name in self.user_attributes:
            value = getattr(user, attribute_name, None)
            if not value or not isinstance(value, str):
                continue
            value_lower = value.lower()
            value_parts = re.split(r'\W+', value_lower) + [value_lower]
            for value_part in value_parts:
                if exceeds_maximum_length_ratio(password, self.max_similarity, value_part):
                    continue
                if SequenceMatcher(a=password, b=value_part).quick_ratio() >= self.max_similarity:
                    try:
                        verbose_name = str(user._meta.get_field(attribute_name).verbose_name)
                    except FieldDoesNotExist:
                        verbose_name = attribute_name
                    raise ValidationError(
                        _("Şifrə %(verbose_name)s ilə çox oxşardır."),
                        code='password_too_similar',
                        params={'verbose_name': verbose_name},
                    )
    def get_help_text(self):
        return _('Şifrəniz digər şəxsi məlumatlarınızla çox oxşar ola bilməz.')

class CustomCommonPasswordValidator(CommonPasswordValidator):

    def validate(self, password, user=None):
        if password.lower().strip() in self.passwords:
            raise ValidationError(
                _("Bu şifrə çox istifadə olunandır."),
                code='password_too_common',
            )

    def get_help_text(self):
        return _('Şifrəniz çox istifadə edilən parol ola bilməz.')
