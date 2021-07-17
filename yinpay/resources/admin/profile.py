from flask_jwt_extended import jwt_required, current_user
from flask_restplus import Resource, Namespace

from yinpay.schema import ProfileSchema

namespace = Namespace('Profile', description='', path='/profile', decorators=[jwt_required()])

schema = ProfileSchema()


class UserResource(Resource):
    def get(self):
        return schema.dump(current_user)

    def put(self):
        user = schema.load(namespace.payload, instance=current_user, unknown='exclude', )
        user.save()
        return schema.dump(user), 200


namespace.add_resource(UserResource, '/')
