from flask_jwt_extended import current_user
from flask_restplus import Resource, Namespace

from yinpay.ext import flask_filter, pagination, db
from yinpay.models import UserLeave
from yinpay.schema import CurrentUserLeaveSchema

namespace = Namespace('userLeave', path='/user/leave')

schema = CurrentUserLeaveSchema()


class UserLeaveResourceList(Resource):
    def get(self):
        search = current_user.user_meta.user_leaves
        if namespace.payload:
            search = flask_filter.search(current_user.user_meta.user_leaves,
                                         [namespace.payload.get('filters')], CurrentUserLeaveSchema(many=True),
                                         order_by=namespace.payload.get('order_by', 'created'))
        return pagination.paginate(search, schema, marshmallow=True)

    def post(self):
        leave = UserLeave()
        leave = schema.load(namespace.payload, session=db.session, instance=leave, unknown='exclude')
        leave.save()
        return schema.dump(leave), 200


class UserLeaveResource(Resource):
    def get(self, pk):
        leave = current_user.user_meta.user_leaves.filter(UserLeave.id == pk).first_or_404()
        return schema.dump(leave), 200

    def put(self, pk):
        leave = current_user.user_meta.user_leaves.filter(UserLeave.id == pk).first_or_404()
        leave = schema.load(namespace.payload, session=db.session, instance=leave, unknown='exclude')
        leave.save()
        return schema.dump(leave), 200

    def delete(self, pk):
        leave = current_user.user_meta.user_leaves.filter(UserLeave.id == pk).first_or_404()
        return leave.delete(), 200
