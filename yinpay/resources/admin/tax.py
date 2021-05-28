from flask_jwt_extended import jwt_required, current_user
from flask_restplus import Resource, Namespace

from yinpay import flask_filter, pagination, db
from yinpay.common.localns import selector
from yinpay.models import Tax
from yinpay.schema import TaxSchema

namespace = Namespace('tax', path='/tax', decorators=[jwt_required()])
schema = TaxSchema()


class TaxListResource(Resource):
    @namespace.expect(selector)
    def get(self):
        sel = selector.parse_args()
        search = current_user.business.filter_by(id=sel.selector).first_or_404().taxes
        if namespace.payload:
            search = flask_filter.search(current_user.business.filter_by(id=sel.selector).first_or_404().taxes,
                                         [namespace.payload.get('filters')], TaxSchema(many=True),
                                         order_by=namespace.payload.get('order_by', 'created'))
        return pagination.paginate(search, schema, marshmallow=True)

    @namespace.expect(selector)
    def post(self):
        sel = selector.parse_args()
        bs = current_user.business.filter_by(id=sel.selector).first_or_404()
        tax = Tax()
        namespace.payload['business_id'] = bs.id
        tax = schema.load(namespace.payload, session=db.session, instance=tax, unknown='exclude')
        tax.save()
        return schema.dump(tax), 200


class TaxResource(Resource):
    @namespace.expect(selector)
    def get(self, pk):
        sel = selector.parse_args()
        bs = current_user.business.filter_by(id=sel.selector).first_or_404()
        tax = Tax.query.filter(Tax.id == pk, Tax.business_id == bs.id).first_or_404()
        return schema.dump(tax), 200

    @namespace.expect(selector)
    def put(self, pk):
        sel = selector.parse_args()
        bs = current_user.business.filter_by(id=sel.selector).first_or_404()
        tax = Tax.query.filter(Tax.id == pk, Tax.business_id == bs.id).first_or_404()
        namespace.payload['business_id'] = bs.id
        tax = schema.load(namespace.payload, session=db.session, instance=tax, unknown='exclude')
        tax.save()
        return schema.dump(tax), 200

    @namespace.expect(selector)
    def delete(self, pk):
        sel = selector.parse_args()
        bs = current_user.business.filter_by(id=sel.selector).first_or_404()
        tax = Tax.query.filter(Tax.id == pk, Tax.business_id == bs.id).first_or_404()
        return tax.delete(), 200


namespace.add_resource(TaxListResource, '/')
namespace.add_resource(TaxResource, '/<pk>')
