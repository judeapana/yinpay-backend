from flask_jwt_extended import jwt_required
from flask_restplus import Resource, Namespace

from yinpay.ext import flask_filter, pagination, db
from yinpay.models import DailyRate
from yinpay.schema import DailyRateSchema

namespace = Namespace('DailyRate', path='/daily-rate',decorators=[jwt_required()])
schema = DailyRateSchema()


class DailyRateListResource(Resource):
    def get(self):
        search = DailyRate
        if namespace.payload:
            search = flask_filter.search(DailyRate, [namespace.payload.get('filters')], DailyRateSchema(many=True),
                                         order_by=namespace.payload.get('order_by', 'created'))
        return pagination.paginate(search, schema, marshmallow=True)

    def post(self):
        dr = DailyRate()
        dr = schema.load(namespace.payload, session=db.session, instance=dr, unknown='exclude')
        dr.save()
        return schema.dump(dr), 200


class DailyRateResource(Resource):
    def get(self, pk):
        dr = DailyRate.query.get_or_404(pk)
        return dr, 200

    def put(self, pk):
        dr = DailyRate.query.get_or_404(pk)
        dr = schema.load(namespace.payload, session=db.session, instance=dr, unknown='exclude')
        dr.save()
        return schema.dump(dr), 200

    def delete(self, pk):
        dr = DailyRate.query.get_or_404(pk)
        return dr.delete(), 200


namespace.add_resource(DailyRateListResource, '/')
namespace.add_resource(DailyRateResource, '/<pk>')
