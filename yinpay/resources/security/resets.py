from flask_restplus import Resource, fields, inputs
from flask_restplus.reqparse import RequestParser

from yinpay import User
from yinpay.common.exceptions import ValidationError
from yinpay.common.helpers import flash
from yinpay.common.validators import password
from yinpay.resources.security import namespace
from yinpay.tasks import send_mail

model = namespace.model('Reset', {
    'email_address': fields.String()
})
parser = RequestParser(trim=True, bundle_errors=True)
parser.add_argument('email_address', required=True, type=inputs.email(), location='json')
parser.add_argument('password', required=True, type=password, location='json')
parser.add_argument('token', required=True, type=str, location='json')


class ResetPwd(Resource):
    def get(self):
        """
        reset user password [Validating Token on GET]
        :return:
        """
        parser.remove_argument('email_address')
        parser.remove_argument('password')
        res = parser.parse_args()
        token = User.authenticate_token(res.token)
        if token:
            return flash(message='link is expired or already used'), 400
        user = User.query.filter(User.id == token.get('id')).one_or_none()
        if not user:
            return flash(message='User could not be found'), 400
        if not user.disabled:
            return flash(message='Your account is already active')
        return flash(message=True)

    def put(self):
        """
        complete reset of user password [Validate Token on PUT]
        :return:
        """
        parser.remove_argument('email_address')
        res = parser.parse_args()
        token = User.authenticate_token(res.token)
        if token:
            return flash(message='link is expired or already used'), 400
        user = User.query.filter(User.id == token.get('id')).one_or_none()
        if not user:
            return flash(message='User could not be found'), 400
        if not user.disabled:
            return flash(message='Your account is already active')
        user.set_password(res.password)
        user.save()
        return flash(message='password reset successful')


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
            errors['email_address'] = "Your email address isn't registered"
        if errors:
            raise ValidationError(message=errors)
        send_mail.queue()
        return flash(message='Reset link has been sent to your account'), 200


namespace.add_resource(ResetPwd, '/reset-pwd', endpoint='reset_pwd')
namespace.add_resource(ForgotPassword, '/forgot-pwd', endpoint='forgot_pwd')
