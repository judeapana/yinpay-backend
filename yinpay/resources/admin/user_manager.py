from flask_jwt_extended import jwt_required
from flask_restplus import Resource, Namespace, fields

from yinpay.ext import pagination, flask_filter, db
from yinpay.models import User
from yinpay.schema import UserSchema, EmailAddressSchema, PasswordSchema

namespace = Namespace('user_management', description='', path='/users', decorators=[jwt_required()])

schema = UserSchema()

model = namespace.model('UserManagement', {
    'username': fields.String(),
    'password': fields.String(),
    'first_name': fields.String(),
    'last_name': fields.String(),
    'email_address': fields.String(),
    'phone_number': fields.String(),
    'disabled': fields.Boolean(),
    'superuser': fields.Boolean(),
    'hrm_support': fields.Boolean(),
    'payroll_support': fields.Boolean(),
    'notes': fields.String()
})


class UserManagerListResource(Resource):

    def get(self):
        search = User
        if namespace.payload:
            search = flask_filter.search(User, [namespace.payload.get('filters')], UserSchema(many=True),
                                         order_by=namespace.payload.get('order_by', 'created'))
        return pagination.paginate(search, schema, marshmallow=True)

    @namespace.expect(model)
    def post(self):
        user = User()
        user = schema.load(namespace.payload, session=db.session, instance=user, unknown='exclude')
        user.set_password(user.password)
        user.save()
        return schema.dump(user), 200


class UserManagerResource(Resource):
    def get(self, pk):
        user = User.query.get_or_404(pk)
        return schema.dump(user), 200

    @namespace.expect(model)
    def put(self, pk):
        user = User.query.get_or_404(pk)
        user = schema.load(namespace.payload, session=db.session, instance=user, unknown='exclude')
        user.save()
        return schema.dump(user), 200

    def delete(self, pk):
        user = User.query.get_or_404(pk)
        user.delete(), 202


class UserPwdResource(Resource):
    def put(self, pk):
        user = User.query.get_or_404(pk)
        pwd_schema = PasswordSchema()
        user = pwd_schema.load(namespace.payload, session=db.session, instance=user, unknown='exclude')
        user.set_password(namespace.payload.get('password'))
        user.save()
        return schema.dump(user), 200


class UserEmailResource(Resource):
    def put(self, pk):
        user = User.query.get_or_404(pk)
        email_schema = EmailAddressSchema()
        user = email_schema.load(namespace.payload, session=db.session, instance=user, unknown='exclude')
        user.email_address = namespace.payload.get('email_address')
        user.save()
        return schema.dump(user), 200


namespace.add_resource(UserManagerListResource, '/')
namespace.add_resource(UserManagerResource, '/<pk>')
namespace.add_resource(UserPwdResource, '/<pk>/change-pwd')
namespace.add_resource(UserPwdResource, '/<pk>/change-email-address')
