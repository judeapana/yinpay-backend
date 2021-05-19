from flask import jsonify, current_app
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, create_refresh_token, current_user, \
    get_jwt
from flask_restplus import Resource, abort, fields
from flask_restplus.reqparse import RequestParser

from yinpay.ext import bcrypt, redis
from yinpay.models import User
from yinpay.resources.security import namespace
from yinpay.schema import UserSchema

parser = RequestParser(trim=True, bundle_errors=True)

parser.add_argument('username', required=True, type=str, location='json')
parser.add_argument('password', required=True, type=str, location='json')

model = namespace.model('Auth', {
    'username': fields.String(),
    'password': fields.String(),
})
schema = UserSchema()


class Login(Resource):
    @namespace.expect(model)
    def post(self):
        """
        Login users with jwt
        :return:
        """
        res = parser.parse_args(strict=True)
        user = User.query.filter((User.email_address == res.username) | (User.username == res.username)).first()
        if not user:
            return abort(401)
        else:
            if not bcrypt.check_password_hash(user.password, res.password):
                return abort(401)
            else:
                if user.disabled:
                    return abort(401,
                                 message='Your account is not active, to activate it request account activation link')
                else:
                    added_claims = schema.dump(obj=user)
                    access_token = create_access_token(identity=user, additional_claims=added_claims)
                    refresh_token = create_refresh_token(identity=user, additional_claims=added_claims)
                    return jsonify(access_token=access_token, refresh_token=refresh_token)


class Refresh(Resource):
    @jwt_required(refresh=True)
    def post(self):
        # TODO: In frontend track time for jwt to expire
        """
        refresh token when access token is about to expire or has expired
        :return:
        """
        identity = get_jwt_identity()
        added_claims = schema.dumps(obj=current_user)
        access_token = create_access_token(identity, additional_claims=added_claims)
        return jsonify(access_token=access_token)


class Logout(Resource):
    @jwt_required
    def post(self):
        """
        Logout user and setting jwt to redis [TTL] to blacklist token
        :return:
        """
        jwt_token_identity = get_jwt()['jti']
        redis.set(jwt_token_identity, "", ex=current_app.config['JWT_ACCESS_TOKEN_EXPIRES'])
        return jsonify(message='Your session is closed')


namespace.add_resource(Login, '/', endpoint='login')
namespace.add_resource(Refresh, '/refresh', endpoint='refresh')
namespace.add_resource(Logout, '/logout', endpoint='logout')
