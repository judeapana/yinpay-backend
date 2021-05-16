from flask_restplus import Resource, Namespace

from yinpay import flask_filter, pagination, db
from yinpay.models import Period
from yinpay.schema import PeriodSchema

namespace = Namespace('Period', path='/period')

schema = PeriodSchema()


class PeriodListResource(Resource):
    def get(self):
        search = Period
        if namespace.payload:
            search = flask_filter.search(Period, [namespace.payload.get('filters')], PeriodSchema(many=True),
                                         order_by=namespace.payload.get('order_by', 'created'))
        return pagination.paginate(search, schema, marshmallow=True)

    def post(self):
        period = Period()
        period = schema.load(namespace.payload, session=db.session, instance=period, unknown='exclude')
        period.save()
        return schema.dump(period), 200


class PeriodResource(Resource):
    def get(self, pk):
        pass

    def put(self, pk):
        pass

    def delete(self, pk):
        pass


namespace.add_resource(PeriodListResource, '/')
namespace.add_resource(PeriodResource, '/<pk>')
