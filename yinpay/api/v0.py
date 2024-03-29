from http import HTTPStatus

from flask import Blueprint, current_app
from flask import g
from flask_restplus import Api, abort
from jwt import ExpiredSignatureError
from marshmallow.exceptions import ValidationError as MarshmallowErrors

from yinpay.common.exceptions import FlashError
from yinpay.common.helpers import validation_error
from yinpay.common.localns import namespace as local_ns
from yinpay.resources.admin import business, user_manager, department, bank, bank_detail, business_account, memo, \
    next_of_kin, period, attendance, daily_rate, working_day, social_security_rate, tax, user_leave, earning_group, \
    deduction_group, user_deduction, user_earning, user_attendance, upload, user_doc, settings, profile, reports
from yinpay.resources.admin import personnel_group
from yinpay.resources.security import namespace as auth

yinapi = Blueprint('api', __name__)

authorizations = {
    'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    }
}
api = Api(yinapi, title='YinPay API', authorizations=authorizations, security='apikey')

api.add_namespace(auth, '/auth')
api.add_namespace(user_manager)
api.add_namespace(department)
api.add_namespace(business_account)
api.add_namespace(memo)
api.add_namespace(next_of_kin)
api.add_namespace(daily_rate)
api.add_namespace(attendance)
api.add_namespace(upload)
api.add_namespace(user_doc)
api.add_namespace(settings)
api.add_namespace(working_day)
api.add_namespace(social_security_rate)
api.add_namespace(user_attendance)
api.add_namespace(tax)
api.add_namespace(user_leave)
api.add_namespace(earning_group)
api.add_namespace(deduction_group)
api.add_namespace(user_deduction)
api.add_namespace(user_earning)
api.add_namespace(period)
api.add_namespace(personnel_group)
api.add_namespace(business)
api.add_namespace(bank_detail)
api.add_namespace(bank)
api.add_namespace(local_ns)
api.add_namespace(profile)
api.add_namespace(reports)


@yinapi.before_request
def watcher():
    if current_app.config['DEBUG']:
        g.frontend = 'https://localhost:8080'
    else:
        g.frontend = 'https://yinpay.yinime.com'


@yinapi.errorhandler(FlashError)
def flash_error(f):
    abort(HTTPStatus.BAD_REQUEST, 'Flash message error', flash=f.messages)


@yinapi.errorhandler(MarshmallowErrors)
def marshmallow_errors(errors):
    return validation_error(errors=errors.messages, code=400)


@yinapi.errorhandler(ExpiredSignatureError)
def expired(f):
    abort(HTTPStatus.UNAUTHORIZED)
