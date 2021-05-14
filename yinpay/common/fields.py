from flask import url_for
from flask_restplus.fields import Raw


class ProtectedField(Raw):
    """
        Format url to /protected path
    """

    def format(self, value):
        if not value:
            return ''
        return url_for('api.protected_dir', filename=value, _external=True)


class StringField(Raw):
    def format(self, value):
        if len(value) <= 0:
            raise ValueError('value is required')
        return value
