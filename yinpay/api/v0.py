from http import HTTPStatus

from flask import Blueprint
from flask_restplus import Api, abort
from marshmallow.exceptions import ValidationError as MarshmallowErrors

from yinpay.common.exceptions import ValidationError, FlashError
from yinpay.resources.admin import attendance, user_manager, business
from yinpay.resources.security import namespace as auth

yinapi = Blueprint('api', __name__)

# authorizations = {
#     'Basic Auth': {
#         'type': 'basic',
#         'in': 'header',
#         'name': 'Authorization'
#     },
# }
authorizations = {
    'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    }
}
api = Api(yinapi, title='YinPay API', authorizations=authorizations, security='apiKey')

api.add_namespace(auth, '/auth')
api.add_namespace(attendance)
api.add_namespace(user_manager)
api.add_namespace(business)


@yinapi.errorhandler(ValidationError)
def schema_errors(errors):
    abort(HTTPStatus.BAD_REQUEST, 'Input validation failed', errors=errors.messages)


@yinapi.errorhandler(FlashError)
def flash_error(f):
    abort(HTTPStatus.BAD_REQUEST, 'Flash message error', flash=f.messages)


@yinapi.errorhandler(MarshmallowErrors)
def marshmallow_errors(errors):
    abort(HTTPStatus.BAD_REQUEST, 'Input validation failed', errors=errors.messages)
