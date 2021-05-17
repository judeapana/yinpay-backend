from flask_restplus import Resource, Namespace

from yinpay import flask_filter, pagination, db
from yinpay.models import Attendance
from yinpay.schema import AttendanceSchema

namespace = Namespace('attendance', description='', path='/attendance')

schema = AttendanceSchema()


class AttendanceListResource(Resource):
    def get(self):
        search = Attendance
        if namespace.payload:
            search = flask_filter.search(Attendance, [namespace.payload.get('filters')], AttendanceSchema(many=True),
                                         order_by=namespace.payload.get('order_by', 'created'))
        return pagination.paginate(search, schema, marshmallow=True)

    def post(self):
        attendance = Attendance()
        attendance = schema.load(namespace.payload, session=db.session, instance=attendance, unknown='exclude')
        attendance.save()
        return schema.dump(attendance), 200


class AttendanceResource(Resource):
    def get(self, pk):
        attendance = Attendance.query.get_or_404(pk)
        return schema.dump(attendance), 200

    def put(self, pk):
        attendance = Attendance.query.get_or_404(pk)
        attendance = schema.load(namespace.payload, session=db.session, instance=attendance, unknown='exclude')
        attendance.save()
        return schema.dump(attendance), 200

    def delete(self, pk):
        attendance = Attendance.query.get_or_404(pk)
        attendance.delete(), 202


namespace.add_resource(AttendanceResource, '/<uuid>', endpoint='')
namespace.add_resource(AttendanceListResource, '/', endpoint='')
