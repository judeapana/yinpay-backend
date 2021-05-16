from flask_restplus import Resource, fields, inputs
from flask_restplus.reqparse import RequestParser

from yinpay.tasks import send_mail
from . import namespace
from ... import User
from ...common.exceptions import ValidationError
from ...common.helpers import flash

model = namespace.model('Account', {
    'email_address': fields.String()
})

parser = RequestParser(trim=True, bundle_errors=True)
parser.add_argument('email_address', required=True, type=inputs.email(), location='json')
parser.add_argument('change_email_address', required=True, type=inputs.email(), location='json')
parser.add_argument('token', required=True, type=str, location='args')


class AccountActivation(Resource):
    @namespace.expect(model)
    def post(self):
        errors = dict()
        parser.remove_argument('token')
        parser.remove_argument('change_email_address')
        res = parser.parse_args()
        user = User.query.filter(User.email_address == res.email_address).first()
        if not user:
            errors['email_address'] = "Your email address isn't registered"
        if errors:
            raise ValidationError(message=errors)
        if not user.disabled:
            return flash(message='Your account is already active')
        send_mail.queue()
        return flash(message='Account activation sent'), 200

    def put(self):
        """
        Activate account
        :return:
        """
        parser.remove_argument('email_address')
        parser.remove_argument('change_email_address')
        res = parser.parse_args()
        token = User.authenticate_token(res.token)
        if token:
            return flash(message='link is expired or already used')
        user = User.query.filter(User.id == token.get('id')).one_or_none()
        if not user:
            return flash(message='User could not be found')
        if not user.disabled:
            return flash(message='Your account is already active')

        user.disabled = False
        user.save()
        return flash(message='Your account has been activated')


class ChangeAccountEmail(Resource):
    @namespace.expect(model)
    def post(self):
        errors = dict()
        parser.remove_argument('token')
        res = parser.parse_args()
        user = User.query.filter(User.email_address == res.email_address).first()
        if not user:
            errors['email_address'] = "Your email address isn't registered"
        if errors:
            return ValidationError(message=errors)
        if user.disabled:
            return flash(message='Your account is disabled')
        send_mail.queue()
        return flash(message='Reset link has been sent to your email address'), 200

    def put(self):
        parser.remove_argument('email_address')
        parser.remove_argument('change_email_address')
        res = parser.parse_args()
        token = User.authenticate_token(res.token)
        if token:
            raise flash(message='link is expired or already used')
        user = User.query.filter(User.id == token.get('id')).one_or_none()
        if not user:
            return flash(message='User could not be found'), 404
        if user.disabled:
            return flash(message='Your account is disabled')
        user.email_address = token.get('email_address')


namespace.add_resource(AccountActivation, '/activate-account', endpoint='activate_account')
namespace.add_resource(ChangeAccountEmail, '/change-email', endpoint='change_email')
