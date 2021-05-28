from flask_jwt_extended import jwt_required, current_user
from flask_restplus import Resource, Namespace

from yinpay.common.localns import selector
from yinpay.ext import flask_filter, pagination, db
from yinpay.models import Attendance
from yinpay.schema import AttendanceSchema

namespace = Namespace('attendance', description='', path='/attendance', decorators=[jwt_required()])

schema = AttendanceSchema()


class AttendanceListResource(Resource):
    @namespace.expect(selector)
    def get(self):
        res = selector.parse_args()
        search = current_user.business.filter_by(id=res.selector).first_or_404().attendances
        if namespace.payload:
            search = flask_filter.search(current_user.business.filter_by(id=res.selector).first_or_404().attendances,
                                         [namespace.payload.get('filters')], AttendanceSchema(many=True),
                                         order_by=namespace.payload.get('order_by', 'created'))
        return pagination.paginate(search, schema, marshmallow=True)

    @namespace.expect(selector)
    def post(self):
        res = selector.parse_args()
        bs = current_user.business.filter_by(id=res.selector).first_or_404()
        attendance = Attendance()
        namespace.payload['business_id'] = bs.id
        attendance = schema.load(namespace.payload, session=db.session, instance=attendance, unknown='exclude')
        attendance.save()
        return schema.dump(attendance), 200


class AttendanceResource(Resource):
    @namespace.expect(selector)
    def get(self, pk):
        res = selector.parse_args()
        bs = current_user.business.filter_by(id=res.selector).first_or_404()
        attendance = Attendance.query.filter(Attendance.id == pk, Attendance.business_id == bs.id).first_or_404()
        return schema.dump(attendance), 200

    @namespace.expect(selector)
    def put(self, pk):
        res = selector.parse_args()
        bs = current_user.business.filter_by(id=res.selector).first_or_404()
        attendance = Attendance.query.filter(Attendance.id == pk, Attendance.business_id == bs.id).first_or_404()
        namespace.payload['business_id'] = bs.id
        attendance = schema.load(namespace.payload, session=db.session, instance=attendance, unknown='exclude')
        attendance.save()
        return schema.dump(attendance), 200

    @namespace.expect(selector)
    def delete(self, pk):
        res = selector.parse_args()
        bs = current_user.business.filter_by(id=res.selector).first_or_404()
        attendance = Attendance.query.filter(Attendance.id == pk, Attendance.business_id == bs.id).first_or_404()
        attendance.delete(), 202


namespace.add_resource(AttendanceResource, '/<pk>', endpoint='')
namespace.add_resource(AttendanceListResource, '/', endpoint='')
