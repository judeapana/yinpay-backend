from flask import request
from flask_jwt_extended import jwt_required, current_user
from flask_restplus import Resource, Namespace, fields

from yinpay.common.localns import selector
from yinpay.ext import pagination, flask_filter, db
from yinpay.models import User, UserMeta
from yinpay.schema import UserSchema, EmailAddressSchema, PasswordSchema

namespace = Namespace('user_management', description='', path='/users', decorators=[jwt_required()])

schema = UserSchema()
user_model = namespace.clone('User', {
    'username': fields.String(),
    'password': fields.String(),
    'first_name': fields.String(),
    'last_name': fields.String(),
    'role': fields.String(),
    'email_address': fields.String(),
    'phone_number': fields.String(),
    'disabled': fields.Boolean(),
    'superuser': fields.Boolean(),
    'hrm_support': fields.Boolean(),
    'payroll_support': fields.Boolean(),
    'notes': fields.String()
})
model = namespace.clone('UserManagement', {
    'user': fields.Nested(user_model),

})

parser = namespace.parser()
parser.add_argument('selector', required=True, type=str, location='args')


class UserManagerListResource(Resource):
    @namespace.expect(selector)
    @namespace.expect(parser)
    def get(self):
        res = parser.parse_args()

        search = User.query.filter(User.user_meta.has(business_id=res.selector), User.role == 'USER')
        if namespace.payload:
            search = flask_filter.search(
                User.query.filter(User.user_meta.has(business_id=res.selector), User.role == 'USER'),
                UserSchema(many=True),
                order_by=namespace.payload.get('order_by', 'created'))
        return pagination.paginate(search, schema, marshmallow=True)

    @namespace.expect(selector)
    @namespace.expect(model)
    def post(self):
        business = current_user.business.filter_by(id=request.args.get('selector')).first_or_404()
        user_schema = UserSchema()
        user = user_schema.load(namespace.payload, session=db.session, unknown='include')
        user.user_meta = UserMeta(business_id=business.id)
        user.set_password(user.password)
        user.save()
        return user_schema.dump(user), 200


class UserManagerResource(Resource):
    def get(self, pk):
        user = User.query.filter(User.role == 'USER', User.id == pk,
                                 User.user_meta.has(business_id=request.args.get('selector'))).first_or_404()
        return schema.dump(user), 200

    @namespace.expect(model)
    @namespace.expect(selector)
    def put(self, pk):
        bs = current_user.business.filter_by(id=request.args.get('selector')).first_or_404()
        if namespace.payload.get('user_meta'):
            namespace.payload['user_meta']['business_id'] = bs.id
        user_schema = UserSchema()
        _user = User.query.filter(User.user_meta.has(business_id=bs.id), User.role == 'USER',
                                  User.id == pk).first_or_404()
        user = user_schema.load(namespace.payload, session=db.session, instance=_user, unknown='include')
        user = schema.load(namespace.payload, session=db.session, instance=user, unknown='include')
        user.save()
        return schema.dump(user), 200

    def delete(self, pk):
        bs = current_user.business.filter_by(id=request.args.get('selector')).first_or_404()
        user = User.query.filter(User.role == 'USER', User.id == pk,
                                 User.user_meta.has(business_id=bs.id)).first_or_404()
        user.delete(), 202


class UserPwdResource(Resource):
    def put(self, pk):
        bs = current_user.business.filter_by(id=request.args.get('selector')).first_or_404()
        user = User.query.filter(User.id == pk, User.user_meta.has(business_id=bs.id)).first_or_404()
        pwd_schema = PasswordSchema()
        pass_wd = pwd_schema.load(namespace.payload, session=db.session, instance=user, unknown='exclude')
        user.set_password(pass_wd.get('password'))
        user.save()
        return schema.dump(user), 200


class UserEmailResource(Resource):
    def put(self, pk):
        bs = current_user.business.filter_by(id=request.args.get('selector')).first_or_404()
        user = User.query.filter(User.id == pk, User.user_meta.has(business_id=bs.id)).first_or_404()
        email_schema = EmailAddressSchema()
        email = email_schema.load(namespace.payload, session=db.session, instance=user, unknown='exclude')
        user.email_address = email.get('email_address')
        user.save()
        return schema.dump(user), 200


namespace.add_resource(UserManagerListResource, '/')
namespace.add_resource(UserManagerResource, '/<pk>')
namespace.add_resource(UserPwdResource, '/<pk>/change-pwd')
namespace.add_resource(UserEmailResource, '/<pk>/change-email-address')
