from flask_jwt_extended import jwt_required, current_user
from flask_restplus import Resource, Namespace

from yinpay import flask_filter, pagination, db
from yinpay.common.localns import selector
from yinpay.models import UserAttendance
from yinpay.schema import UserAttendanceSchema

namespace = Namespace('user_attendance', path='/user-attendance', decorators=[jwt_required()])

schema = UserAttendanceSchema()


class UserAttendanceListResource(Resource):
    @namespace.expect(selector)
    def get(self):
        sel = selector.parse_args()
        search = current_user.business.filter_by(id=sel.selector).first_or_404().user_attendances
        if namespace.payload:
            search = flask_filter.search(
                current_user.business.filter_by(id=sel.selector).first_or_404().user_attendances,
                [namespace.payload.get('filters')],
                UserAttendanceSchema(many=True),
                order_by=namespace.payload.get('order_by', 'created'))
        return pagination.paginate(search, schema, marshmallow=True)

    @namespace.expect(selector)
    def post(self):
        sel = selector.parse_args()
        bs = current_user.business.filter_by(id=sel.selector).first_or_404().user_attendances
        ua = UserAttendance()
        namespace.payload['business_id'] = bs.id
        ua = schema.load(namespace.payload, session=db.session, instance=ua, unknown='exclude')
        ua.save()
        return schema.dump(ua), 200


class UserAttendanceResource(Resource):
    @namespace.expect(selector)
    def get(self, pk):
        sel = selector.parse_args()
        bs = current_user.business.filter_by(id=sel.selector).first_or_404()
        ua = UserAttendance.query.filter(UserAttendance.business_id == bs.id, UserAttendance.id == pk).first_or_404()
        return schema.dump(ua), 200

    @namespace.expect(selector)
    def put(self, pk):
        sel = selector.parse_args()
        bs = current_user.business.filter_by(id=sel.selector).first_or_404()
        ua = UserAttendance.query.filter(UserAttendance.business_id == bs.id, UserAttendance.id == pk).first_or_404()
        ua = schema.load(namespace.payload, session=db.session, instance=ua, unknown='exclude')
        ua.save()
        return schema.dump(ua), 200

    @namespace.expect(selector)
    def delete(self, pk):
        sel = selector.parse_args()
        bs = current_user.business.filter_by(id=sel.selector).first_or_404()
        ua = UserAttendance.query.filter(UserAttendance.business_id == bs.id, UserAttendance.id == pk).first_or_404()
        return ua.delete(), 200


namespace.add_resource(UserAttendanceListResource, '/')
namespace.add_resource(UserAttendanceResource, '/<pk>')
