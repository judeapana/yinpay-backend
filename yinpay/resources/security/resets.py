from flask import g
from flask_restplus import Resource, fields, inputs
from flask_restplus.reqparse import RequestParser

from yinpay import User
from yinpay.common.helpers import flash, validation_error
from yinpay.common.validators import password
from yinpay.resources.security import namespace
from yinpay.tasks import send_mail

model = namespace.model('Reset', {
    'email_address': fields.String()
})
reset_model = namespace.model('ResetPwd', {
    'email_address': fields.String(),
    'password': fields.String(),
    'token': fields.String()
})
parser = RequestParser(trim=True, bundle_errors=True)
parser.add_argument('email_address', required=True, type=inputs.email(), location='json')
parser.add_argument('password', required=True, type=password, location='json')
parser.add_argument('token', required=True, type=str, location='json')


class ResetPwd(Resource):
    @namespace.expect(reset_model)
    def post(self):
        """
        reset user password [Validating Token on GET]
        :return:
        """
        parser.remove_argument('email_address')
        parser.remove_argument('password')
        res = parser.parse_args()
        token = User.authenticate_token(res.token)
        if not token:
            return flash(message=['link is expired or already used'], code=400)
        return flash(message=['Token session is active'])

    @namespace.expect(reset_model)
    def put(self):
        """
        complete reset of user password [Validate Token on PUT]
        :return:
        """
        parser.remove_argument('email_address')
        res = parser.parse_args()
        token = User.authenticate_token(res.token)
        if not token:
            return flash(message=['link is expired or already used'], code=400)
        user = User.query.filter(User.id == token.get('id')).one_or_none()
        if not user:
            return flash(message=['User could not be found'], code=400)
        if user.disabled:
            return flash(message=['Your account is not active'], code=400)
        user.set_password(res.password)
        user.save()
        msg = f"""
                Your account password has been successfully reset.
                """
        send_mail.queue('YINPAY Notification', msg, [user.email_address])
        return flash(message=['password reset successful'])


class ForgotPassword(Resource):
    @namespace.expect(model)
    def post(self):
        """
        Assist user send reset details to their email address
        :return:
        :param: email address
        """
        errors = dict()
        parser.remove_argument('token')
        parser.remove_argument('password')
        res = parser.parse_args()
        user = User.query.filter(User.email_address == res.email_address).first()
        if not user:
            errors['email_address'] = ["Your email address isn't registered"]
        if errors:
            return validation_error(errors)
        msg = f"""
                You have request to reset your account password,<br/>
                Goto the provided link below.<br/>
                <a href='{g.frontend}/app/reset-pwd?token={user.create_token()}'>Link</>
                """
        send_mail('YINPAY', msg, [user.email_address])
        return flash(message=['Reset link has been sent to your account'])


namespace.add_resource(ResetPwd, '/reset-pwd', endpoint='reset_pwd')
namespace.add_resource(ForgotPassword, '/forgot-pwd', endpoint='forgot_pwd')
