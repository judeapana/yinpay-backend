import datetime

from flask_jwt_extended import current_user
from flask_restplus import Resource, Namespace

from yinpay.common.exceptions import FlashError
from yinpay.ext import flask_filter, pagination, db
from yinpay.models import Attendance, UserAttendance
from yinpay.schema import CurrentUserAttendanceSchema

namespace = Namespace('userDailyRate', path='/user/attendance')
schema = CurrentUserAttendanceSchema()


class CurUserAttendanceResourceList(Resource):
    def get(self):
        search = current_user.user_meta.attendances
        if namespace.payload:
            search = flask_filter.search(current_user.user_meta.attendances,
                                         [namespace.payload.get('filters')], CurrentUserAttendanceSchema(many=True),
                                         order_by=namespace.payload.get('order_by', 'created'))
        return pagination.paginate(search, schema, marshmallow=True)

    def post(self):
        p_day = Attendance.query.filter(Attendance.day == datetime.datetime.utcnow()).first()
        if not p_day:
            raise FlashError("Current day doesnt have a registered attendance")
        user_At = UserAttendance
        user_att = schema.load(namespace.payload, session=db.session, instance=user_At, unknown='exclude')
        user_att.save()
        return schema.dump(user_att), 200


class CurUserAttendanceResource(Resource):
    def get(self, pk):
        attendance = current_user.user_meta.attendances.filter(UserAttendance.id == pk).first_or_404()
        return schema.dump(attendance), 200

    def delete(self, pk):
        attendance = current_user.user_meta.attendances.filter(UserAttendance.id == pk).first_or_404()
        return attendance.delete(), 200
