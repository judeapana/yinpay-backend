from flask import g
from flask_jwt_extended import jwt_required, current_user
from flask_restplus import Resource, fields, inputs
from flask_restplus.reqparse import RequestParser

from yinpay.tasks import send_mail
from . import namespace
from ... import User
from ...common.helpers import flash

model = namespace.model('Account', {
    'email_address': fields.String(),
    'token': fields.String()
})

parser = RequestParser(trim=True, bundle_errors=True)
parser.add_argument('email_address', required=True, type=inputs.email(), location='json')
parser.add_argument('change_email_address', required=True, type=inputs.email(), location='json')
parser.add_argument('token', required=True, type=str, location='json')


class AccountActivation(Resource):
    @namespace.expect(model)
    def put(self):
        """
        Activate account
        :return:
        """
        parser.remove_argument('email_address')
        parser.remove_argument('change_email_address')
        res = parser.parse_args()
        token = User.authenticate_token(res.token)
        if not token:
            return flash(message=['link is expired or already used'], code=400)
        user = User.query.filter(User.id == token.get('id')).one_or_none()
        if not user:
            return flash(message=['User could not be found'], code=400)
        if not user.disabled:
            return flash(message=['Your account is already active'], code=400)

        user.disabled = False
        user.save()
        msg = f"""
               Your account has been successfully activated.
               """
        send_mail.queue('YINPAY Notification', msg, [user.email_address])
        return flash(message=['Your account has been activated'])


class ChangeAccountEmail(Resource):
    @jwt_required(refresh=False)
    @namespace.expect(model)
    def post(self):
        parser.remove_argument('token')
        res = parser.parse_args()

        if current_user.disabled:
            return flash(message=['Your account is disabled'], code=400)
        msg = f"""
                This email address  [{current_user.email_address}] is processed to be changed to [{res.change_email_address}]<br/>
                Use this link <a href="{g.frontend}/app/change-email?token={current_user.create_token(payload={'change_email_address': res.change_email_address})}">Change now!</a>
               """
        send_mail.queue('YINPAY Notification', msg, [res.get('change_email_address')])
        return flash(message=['Reset link has been sent to your email address'])

    @namespace.expect(model)
    @jwt_required(refresh=False)
    def put(self):
        parser.remove_argument('email_address')
        parser.remove_argument('change_email_address')
        res = parser.parse_args()
        token = User.authenticate_token(res.token)
        if not token:
            return flash(message=['link is expired or already used'], code=400)
        user = User.query.filter(User.id == token.get('id')).one_or_none()
        if not user:
            return flash(message=['User could not be found'], code=400)
        if user.disabled:
            return flash(message=['Your account is disabled'], code=400)
        if not token.get('change_email_address'):
            return flash(['Change to email cant be empty'], 400)
        user.email_address = token.get('change_email_address')
        user.save()
        msg = f"""
            Your account email address has been successfully changed.
             """
        send_mail.queue('YINPAY Notification', msg, [user.email_address ])
        return flash(['Your email has been changed successfully'])


namespace.add_resource(AccountActivation, '/activate-account', endpoint='activate_account')
namespace.add_resource(ChangeAccountEmail, '/change-email', endpoint='change_email')
