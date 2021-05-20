from flask_jwt_extended import jwt_required
from flask_restplus import Resource, Namespace

from yinpay import flask_filter, pagination, db
from yinpay.models import UserAttendance
from yinpay.schema import UserAttendanceSchema

namespace = Namespace('user_attendance', path='/user-attendance',decorators=[jwt_required()])

schema = UserAttendanceSchema()


class UserAttendanceListResource(Resource):
    def get(self):
        search = UserAttendance
        if namespace.payload:
            search = flask_filter.search(UserAttendance, [namespace.payload.get('filters')],
                                         UserAttendanceSchema(many=True),
                                         order_by=namespace.payload.get('order_by', 'created'))
        return pagination.paginate(search, schema, marshmallow=True)

    def post(self):
        ua = UserAttendance()
        ua = schema.load(namespace.payload, session=db.session, instance=ua, unknown='exclude')
        ua.save()
        return schema.dump(ua), 200


class UserAttendanceResource(Resource):
    def get(self, pk):
        ua = UserAttendance.query.get_or_404(pk)
        return ua, 200

    def put(self, pk):
        ua = UserAttendance.query.get_or_404(pk)
        ua = schema.load(namespace.payload, session=db.session, instance=ua, unknown='exclude')
        ua.save()
        return schema.dump(ua), 200

    def delete(self, pk):
        ua = UserAttendance.query.get_or_404(pk)
        return ua.delete(), 200


namespace.add_resource(UserAttendanceListResource, '/')
namespace.add_resource(UserAttendanceResource, '/<pk>')
