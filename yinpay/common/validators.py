import re

from marshmallow import ValidationError


def tel(value):
    if re.fullmatch(r'^[+]?[(]?[0-9]{3}[)]?[-\s.]?[0-9]{3}[-\s.]?[0-9]{4,6}$', value):
        raise ValidationError(f'{value} is not a valid tel must be 10 characters')
    return value


def password(value):
    if re.fullmatch(r'[A-Za-z0-9@#$%^&+=]{8,}', value):
        return value
    raise ValidationError(f'password must be at least 8 characters long')


def character(value):
    if len(value) >= 3:
        return value
    raise ValidationError(f'{value} must be at least 3 characters long')


def username(value):
    if re.fullmatch(r'^[a-zA-Z0-9_]{3,}', value):
        return value
    raise ValidationError('At least 3 letters, numbers and underscore are allowed.')


