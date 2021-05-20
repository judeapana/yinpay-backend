from flask_jwt_extended import jwt_required
from flask_restplus import Resource, Namespace

from yinpay import flask_filter, pagination, db
from yinpay.models import WorkingDay
from yinpay.schema import WorkingDaySchema

namespace = Namespace('working_days', path='/working-day', decorators=[jwt_required()])

schema = WorkingDaySchema()


class WorkingDayResource(Resource):
    def get(self):
        search = WorkingDay
        if namespace.payload:
            search = flask_filter.search(WorkingDay, [namespace.payload.get('filters')], WorkingDaySchema(many=True),
                                         order_by=namespace.payload.get('order_by', 'created'))
        return pagination.paginate(search, schema, marshmallow=True)

    def post(self):
        wd = WorkingDay()
        wd = schema.load(namespace.payload, session=db.session, instance=wd, unknown='exclude')
        wd.save()
        return schema.dump(wd), 200


class WorkingDayResourceList(Resource):
    def get(self, pk):
        wd = WorkingDay.query.get_or_404(pk)
        return wd, 200

    def put(self, pk):
        wd = WorkingDay.query.get_or_404(pk)
        wd = schema.load(namespace.payload, session=db.session, instance=wd, unknown='exclude')
        wd.save()
        return schema.dump(wd), 200

    def delete(self, pk):
        wd = WorkingDay.query.get_or_404(pk)
        return wd.delete(), 200


namespace.add_resource(WorkingDayResource, '/')
namespace.add_resource(WorkingDayResourceList, '/<pk>')
