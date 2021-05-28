from flask_jwt_extended import jwt_required, current_user
from flask_restplus import Resource, Namespace

from yinpay import flask_filter, pagination, db
from yinpay.common.localns import selector
from yinpay.models import UserLeave
from yinpay.schema import UserLeaveSchema

namespace = Namespace('user_leave', path='/user-leave', decorators=[jwt_required()])

schema = UserLeaveSchema()


class UserLeaveListResource(Resource):
    @namespace.expect(selector)
    def get(self):
        sel = selector.parse_args()
        search = current_user.business.filter_by(id=sel.selector).first_or_404().user_leaves
        if namespace.payload:
            search = flask_filter.search(UserLeave, [namespace.payload.get('filters')], UserLeaveSchema(many=True),
                                         order_by=namespace.payload.get('order_by', 'created'))
        return pagination.paginate(search, schema, marshmallow=True)

    @namespace.expect(selector)
    def post(self):
        sel = selector.parse_args()
        bs = current_user.business.filter_by(id=sel.selector).first_or_404()
        user_leave = UserLeave()
        namespace.payload['business_id'] = bs.id
        user_leave = schema.load(namespace.payload, session=db.session, instance=user_leave, unknown='exclude')
        user_leave.save()
        return schema.dump(user_leave), 200


class UserLeaveResource(Resource):
    @namespace.expect(selector)
    def get(self, pk):
        sel = selector.parse_args()
        bs = current_user.business.filter_by(id=sel.selector).first_or_404()
        user_leave = UserLeave.query.filter(UserLeave.business_id == bs.id, UserLeave.id == pk).first_or_404()
        return schema.dump(user_leave), 200

    @namespace.expect(selector)
    def put(self, pk):
        sel = selector.parse_args()
        bs = current_user.business.filter_by(id=sel.selector).first_or_404()
        user_leave = UserLeave.query.filter(UserLeave.business_id == bs.id, UserLeave.id == pk).first_or_404()
        namespace.payload['business_id'] = bs.id
        user_leave = schema.load(namespace.payload, session=db.session, instance=user_leave, unknown='exclude')
        user_leave.save()
        return schema.dump(user_leave), 200

    @namespace.expect(selector)
    def delete(self, pk):
        sel = selector.parse_args()
        bs = current_user.business.filter_by(id=sel.selector).first_or_404()
        user_leave = UserLeave.query.filter(UserLeave.business_id == bs.id, UserLeave.id == pk).first_or_404()
        return user_leave.delete(), 200


namespace.add_resource(UserLeaveListResource, '/')
namespace.add_resource(UserLeaveResource, '/<pk>')
