from flask_restplus import Resource, inputs, fields
from flask_restplus.reqparse import RequestParser

from yinpay import User
from yinpay.common.exceptions import ValidationError
from yinpay.common.helpers import flash
from yinpay.common.validators import tel, password, character, username
from yinpay.resources.security import namespace
from yinpay.tasks import send_mail

model = namespace.model('Register', {
    'username': fields.String(required=True),
    'first_name': fields.String(required=True),
    'last_name': fields.String(),
    'email_address': fields.String(),
    'password': fields.String(),
    'phone_number': fields.String()
})
parser = RequestParser(trim=True, bundle_errors=True)
parser.add_argument('username', required=True, type=username, location='json')
parser.add_argument('first_name', required=True, type=character, location='json')
parser.add_argument('last_name', required=True, type=character, location='json')
parser.add_argument('password', required=True, type=password, location='json')
parser.add_argument('email_address', required=True, type=inputs.email(), location='json')
parser.add_argument('phone_number', required=True, type=tel, location='json')


class Register(Resource):
    @namespace.expect(model)
    def post(self):
        errors = dict()
        res = parser.parse_args()
        user = User.query.filter(User.email_address == res.email_address).first()
        if user:
            errors['email_address'] = ['email address is registered to a different account']
        phone = User.query.filter(User.phone_number == res.phone_number).first()
        if phone:
            errors['phone_number'] = ['phone number already exists']
        user_named = User.query.filter(User.username == res.username).first()
        if user_named:
            errors['username'] = ['username already exists']
        if errors:
            raise ValidationError(message=errors)
        new_user = User(**res, superuser=True, hrm_support=True, payroll_support=True, disabled=True)
        new_user.set_password(res.password)
        new_user.save()
        send_mail.queue()
        return flash(message='Your account has been created')


namespace.add_resource(Register, '/register', endpoint='register')
