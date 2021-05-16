from flask_restplus import Resource, Namespace

from yinpay import flask_filter, pagination, db
from yinpay.models import UserLeave
from yinpay.schema import UserLeaveSchema

namespace = Namespace('user_leave', path='/user-leave')

schema = UserLeaveSchema()


class UserLeaveListResource(Resource):
    def get(self):
        search = UserLeave
        if namespace.payload:
            search = flask_filter.search(UserLeave, [namespace.payload.get('filters')], UserLeaveSchema(many=True),
                                         order_by=namespace.payload.get('order_by', 'created'))
        return pagination.paginate(search, schema, marshmallow=True)

    def post(self):
        user_leave = UserLeave()
        user_leave = schema.load(namespace.payload, session=db.session, instance=user_leave, unknown='exclude')
        user_leave.save()
        return schema.dump(user_leave), 200


class UserLeaveResource(Resource):
    def get(self, pk):
        pass

    def post(self, pk):
        pass

    def delete(self, pk):
        pass


namespace.add_resource(UserLeaveListResource, '/')
namespace.add_resource(UserLeaveResource, '/<pk>')
