import gzip
import re
import string
from difflib import SequenceMatcher
from pathlib import Path
from wtforms.validators import ValidationError


class UserAttributeSimilarity(object):
    """
    Validates whether the password is sufficiently different from the user's
    attributes.
    """
    DEFAULT_USER_ATTRIBUTES = ('username', 'first_name', 'last_name', 'email')

    def __init__(self, user_attributes=DEFAULT_USER_ATTRIBUTES,
                 max_similarity=0.7, message=None):
        self.message = message
        self.user_attributes = user_attributes
        self.max_similarity = max_similarity

    def __call__(self, form, field, user=None):
        message = self.message
        if message is None:
            message = field.gettext('The password is too similar.')

        if not user:
            return

        for attribute_name in self.user_attributes:
            value = getattr(user, attribute_name, None)
            if not value or not isinstance(value, str):
                continue
            value_parts = re.split(r'\W+', value) + [value]
            for value_part in value_parts:
                if SequenceMatcher(
                    a=field.data.lower(), b=value_part.lower()
                ).quick_ratio() >= self.max_similarity:
                    try:
                        verbose_name = str(user._meta.get_field(
                            attribute_name).verbose_name)
                    except Exception:
                        verbose_name = attribute_name
                    raise ValidationError(
                        'The password is too similar to the %s.' % verbose_name)


class CommonPassword(object):
    """
    Validate whether the password is a common password.
    """
    DEFAULT_PASSWORD_LIST_PATH = (
        Path(__file__).resolve().parent / 'common-passwords.txt.gz')

    def __init__(self,
                 password_list_path=DEFAULT_PASSWORD_LIST_PATH, message=None):
        self.message = message
        try:
            with gzip.open(str(password_list_path)) as f:
                common_passwords_lines = f.read().decode().splitlines()
        except OSError:
            with open(str(password_list_path)) as f:
                common_passwords_lines = f.readlines()

        self.passwords = {p.strip() for p in common_passwords_lines}

    def __call__(self, form, field):
        message = self.message
        if message is None:
            message = field.gettext('This password is too common.')

        if field.data.lower().strip() in self.passwords:
            raise ValidationError(message)


class NumericPassword(object):
    """
    Validate whether the password is alphanumeric.
    """

    def __init__(self, message=None):
        self.message = message

    def __call__(self, form, field):
        message = self.message
        if message is None:
            message = field.gettext('This password is entirely numeric.')
        if field.data.isdigit():
            raise ValidationError(message)


class ValidatePassword(object):
    """
    Validate password complexity:
    - at least 1 lowercase character (a-z)
    - at least 1 uppercase character (A-Z)
    - at least 1 digit (\d)
    - at least 1 special character (punctuation) including space
    - not more than 2 identical characters in a row (e.g., 111 not allowed)
    """

    def __init__(self, message=None):
        self.message = message

    def __call__(self, form, field):
        message = self.message
        if message is None:
            message = field.gettext(
                'Your password must include at least one lowercase, '
                'one uppercase, one number, one special character '
                '(punctuation including space), '
                'and not more than 2 identical characters in a row.')
        if not re.search(
                '^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).+$', field.data):
            raise ValidationError(message)
        if not re.search('[' + string.punctuation + ' ' + ']', field.data):
            raise ValidationError(message)
        if re.search(r'(.)\1{2,}', field.data):
            raise ValidationError(message)