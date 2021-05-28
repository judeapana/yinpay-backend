from flask_jwt_extended import jwt_required, current_user
from flask_restplus import Resource, Namespace

from yinpay.common.localns import selector
from yinpay.ext import flask_filter, pagination, db
from yinpay.models import DailyRate
from yinpay.schema import DailyRateSchema

namespace = Namespace('DailyRate', path='/daily-rate', decorators=[jwt_required()])
schema = DailyRateSchema()


class DailyRateListResource(Resource):
    @namespace.expect(selector)
    def get(self):
        sel = selector.parse_args()
        search = current_user.business.filter_by(id=sel.selector).first_or_404().daily_rates
        if namespace.payload:
            search = flask_filter.search(current_user.business.filter_by(id=sel.selector).first_or_404().daily_rates,
                                         [namespace.payload.get('filters')], DailyRateSchema(many=True),
                                         order_by=namespace.payload.get('order_by', 'created'))
        return pagination.paginate(search, schema, marshmallow=True)

    @namespace.expect(selector)
    def post(self):
        sel = selector.parse_args()
        bs = current_user.business.filter_by(id=sel.selector).first_or_404()
        dr = DailyRate()
        namespace.payload['business_id'] = bs.id
        dr = schema.load(namespace.payload, session=db.session, instance=dr, unknown='exclude')
        dr.save()
        return schema.dump(dr), 200


class DailyRateResource(Resource):
    @namespace.expect(selector)
    def get(self, pk):
        sel = selector.parse_args()
        bs = current_user.business.filter_by(id=sel.selector).first_or_404()
        dr = DailyRate.query.filter(DailyRate.business_id == bs.id, DailyRate.id == pk).first_or_404()
        return schema.dump(dr), 200

    @namespace.expect(selector)
    def put(self, pk):
        sel = selector.parse_args()
        bs = current_user.business.filter_by(id=sel.selector).first_or_404()
        dr = DailyRate.query.filter(DailyRate.business_id == bs.id, DailyRate.id == pk).first_or_404()
        namespace.payload['business_id'] = bs.id
        dr = schema.load(namespace.payload, session=db.session, instance=dr, unknown='exclude')
        dr.save()
        return schema.dump(dr), 200

    @namespace.expect(selector)
    def delete(self, pk):
        sel = selector.parse_args()
        bs = current_user.business.filter_by(id=sel.selector).first_or_404()
        dr = DailyRate.query.filter(DailyRate.business_id == bs.id, DailyRate.id == pk).first_or_404()
        return dr.delete(), 200


namespace.add_resource(DailyRateListResource, '/')
namespace.add_resource(DailyRateResource, '/<pk>')
