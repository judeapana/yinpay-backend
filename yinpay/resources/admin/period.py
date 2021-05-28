from flask_jwt_extended import jwt_required, current_user
from flask_restplus import Resource, Namespace

from yinpay.common.localns import selector
from yinpay.ext import flask_filter, pagination, db
from yinpay.models import Period
from yinpay.schema import PeriodSchema

namespace = Namespace('Period', path='/period', decorators=[jwt_required()])

schema = PeriodSchema()


class PeriodListResource(Resource):
    @namespace.expect(selector)
    def get(self):
        res = selector.parse_args()
        search = current_user.business.filter_by(id=res.selector).first_or_404().periods
        if namespace.payload:
            search = flask_filter.search(current_user.business.filter_by(id=res.selector).first_or_404().periods,
                                         [namespace.payload.get('filters')], PeriodSchema(many=True),
                                         order_by=namespace.payload.get('order_by', 'created'))
        return pagination.paginate(search, schema, marshmallow=True)

    @namespace.expect(selector)
    def post(self):
        res = selector.parse_args()
        bs = current_user.business.filter_by(id=res.selector).first_or_404()
        period = Period()
        namespace.payload['business_id'] = bs.id
        period = schema.load(namespace.payload, session=db.session, instance=period, unknown='exclude')
        period.save()
        return schema.dump(period), 200


class PeriodResource(Resource):
    @namespace.expect(selector)
    def get(self, pk):
        res = selector.parse_args()
        bs = current_user.business.filter_by(id=res.selector).first_or_404()
        period = Period.query.filter(Period.id == pk, Period.business_id == bs.id).first_or_404()
        return schema.dump(period), 200

    @namespace.expect(selector)
    def put(self, pk):
        res = selector.parse_args()
        bs = current_user.business.filter_by(id=res.selector).first_or_404()
        period = Period.query.filter(Period.id == pk, Period.business_id == bs.id).first_or_404()
        namespace.payload['business_id'] = bs.id
        period = schema.load(namespace.payload, session=db.session, instance=period, unknown='exclude')
        period.save()
        return schema.dump(period), 200

    @namespace.expect(selector)
    def delete(self, pk):
        res = selector.parse_args()
        bs = current_user.business.filter_by(id=res.selector).first_or_404()
        period = Period.query.filter(Period.id == pk, Period.business_id == bs.id).first_or_404()
        return period.delete(), 200


namespace.add_resource(PeriodListResource, '/')
namespace.add_resource(PeriodResource, '/<pk>')
