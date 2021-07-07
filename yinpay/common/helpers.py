import os
import secrets
from functools import wraps

from PIL import Image
from flask import make_response, jsonify, request, current_app
from flask_jwt_extended import current_user
from flask_restplus import abort
from marshmallow import ValidationError
from werkzeug.utils import secure_filename


def flash(message, code=200):
    return make_response(jsonify(message=message), code)


def validation_error(errors, code=400):
    return make_response(jsonify(message="Input payload validation failed", errors=errors), code)


def get_uuid():
    with current_app.app_context():
        return request.path.split('/')[-1] or None


def img_upload(file_storage, resize=(750, 750), base_dir='protected', allowed=None):
    if allowed is None:
        allowed = ['png', 'jpg', 'jpeg', 'gif']
    filename = secure_filename(file_storage.filename)
    ext = filename.split('.')[-1]
    if not (ext in allowed):
        raise ValidationError({'file': ['file extension not allowed', f'allowed extensions are {allowed}']})
    cur_file_name = f'{secrets.token_hex(20)}.{ext}'
    image = Image.open(file_storage)
    image.thumbnail(resize)
    file_storage.save(os.path.join(current_app.root_path, 'static', f'{base_dir}/{cur_file_name}'))
    return cur_file_name


def delete_file(filename, base_dir='protected'):
    path = os.path.join(current_app.root_path, 'static', f'{base_dir}/{filename}')
    if not os.path.isfile(path):
        return flash('File Not Found', 400)
    os.remove(path)


def file_upload(file_storage, base_dir='protected', allowed=None):
    if allowed is None:
        allowed = ['pdf', 'docx', 'doc', 'zip', 'png', 'jpg', 'jpeg', 'gif']
    filename = secure_filename(file_storage.filename)
    ext = filename.split('.')
    if not (ext[-1] in allowed):
        raise ValidationError({'file': ['file extension not allowed', f'allowed extensions are {allowed}']})
    cur_file_name = f'{"".join(ext[:-1])}_{secrets.token_hex(20)}.{ext[-1]}'
    file_storage.save(os.path.join(current_app.root_path, 'static', f'{base_dir}/{cur_file_name}'))
    return cur_file_name


def super_user_required():
    def wrapper(func):
        @wraps(func)
        def decorate(*args, **kwargs):
            if not current_user.superuser:
                return abort(401)
            return func(*args, **kwargs)

        return decorate

    return wrapper
