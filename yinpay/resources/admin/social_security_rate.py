from flask_jwt_extended import jwt_required, current_user
from flask_restplus import Resource, Namespace

from yinpay import flask_filter, pagination, db
from yinpay.common.localns import selector
from yinpay.models import SocialSecurityRate
from yinpay.schema import SocialSecurityRateSchema

namespace = Namespace('ssr', path='/ssr', decorators=[jwt_required()])

schema = SocialSecurityRateSchema()


class SocialSrListResource(Resource):
    @namespace.expect(selector)
    def get(self):
        sel = selector.parse_args()
        search = current_user.business.filter_by(id=sel.selector).first_or_404().social_security_rates
        if namespace.payload:
            search = flask_filter.search(
                current_user.business.filter_by(id=sel.selector).first_or_404().social_security_rates,
                [namespace.payload.get('filters')],
                SocialSecurityRateSchema(many=True),
                order_by=namespace.payload.get('order_by', 'created'))
        return pagination.paginate(search, schema, marshmallow=True)

    @namespace.expect(selector)
    def post(self):
        sel = selector.parse_args()
        bs = current_user.business.filter_by(id=sel.selector).first_or_404()
        ssr = SocialSecurityRate()
        namespace.payload['business_id'] = bs.id
        ssr = schema.load(namespace.payload, session=db.session, instance=ssr, unknown='exclude')
        ssr.save()
        return schema.dump(ssr), 200


class SocialSrResource(Resource):
    @namespace.expect(selector)
    def get(self, pk):
        sel = selector.parse_args()
        bs = current_user.business.filter_by(id=sel.selector).first_or_404()
        ssr = SocialSecurityRate.query.filter(SocialSecurityRate.business_id == bs.id,
                                              SocialSecurityRate.id == pk).first_or_404()
        return schema.dump(ssr), 200

    @namespace.expect(selector)
    def put(self, pk):
        sel = selector.parse_args()
        bs = current_user.business.filter_by(id=sel.selector).first_or_404()
        namespace.payload['business_id'] = bs.id
        ssr = SocialSecurityRate.query.filter(SocialSecurityRate.business_id == bs.id,
                                              SocialSecurityRate.id == pk).first_or_404()
        ssr = schema.load(namespace.payload, session=db.session, instance=ssr, unknown='exclude')
        ssr.save()
        return schema.dump(ssr), 200

    @namespace.expect(selector)
    def delete(self, pk):
        sel = selector.parse_args()
        bs = current_user.business.filter_by(id=sel.selector).first_or_404()
        ssr = SocialSecurityRate.query.filter(SocialSecurityRate.business_id == bs.id,
                                              SocialSecurityRate.id == pk).first_or_404()
        return ssr.delete(), 200


namespace.add_resource(SocialSrListResource, '/')
namespace.add_resource(SocialSrResource, '/<pk>')
