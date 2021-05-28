from flask_jwt_extended import jwt_required, current_user
from flask_restplus import Resource, Namespace

from yinpay.common.localns import selector
from yinpay.ext import flask_filter, pagination, db
from yinpay.models import BusinessAccount
from yinpay.schema import BusinessAccountSchema

namespace = Namespace('BusinessAccount', path='/ba', description='', decorators=[jwt_required()])

schema = BusinessAccountSchema()


class BusinessAccountListResource(Resource):
    @namespace.expect(selector)
    def get(self):
        res = selector.parse_args()
        search = current_user.business.filter_by(id=res.selector).first_or_404().business_accounts
        if namespace.payload:
            search = flask_filter.search(
                current_user.business.filter_by(id=res.selector).first_or_404().business_accounts,
                [namespace.payload.get('filters')],
                BusinessAccountSchema(many=True),
                order_by=namespace.payload.get('order_by', 'created'))
        return pagination.paginate(search, schema, marshmallow=True)

    @namespace.expect(selector)
    def post(self):
        res = selector.parse_args()
        bs = current_user.business.filter_by(id=res.selector).first_or_404()
        ba = BusinessAccount()
        namespace.payload['business_id'] = bs.id
        ba = schema.load(namespace.payload, session=db.session, instance=ba, unknown='exclude')
        ba.save()
        return schema.dump(ba), 200


class BusinessAccountResource(Resource):
    @namespace.expect(selector)
    def get(self, pk):
        res = selector.parse_args()
        bs = current_user.business.filter_by(id=res.selector).first_or_404()
        ba = BusinessAccount.query.filter(BusinessAccount.business_id == bs.id, BusinessAccount.id == pk).first_or_404()
        return schema.dump(ba), 200

    @namespace.expect(selector)
    def put(self, pk):
        res = selector.parse_args()
        bs = current_user.business.filter_by(id=res.selector).first_or_404()
        ba = BusinessAccount.query.filter(BusinessAccount.business_id == bs.id, BusinessAccount.id == pk).first_or_404()
        namespace.payload['business_id'] = bs.id
        ba = schema.load(namespace.payload, session=db.session, instance=ba, unknown='exclude')
        ba.save()
        return schema.dump(ba), 200

    @namespace.expect(selector)
    def delete(self, pk):
        res = selector.parse_args()
        bs = current_user.business.filter_by(id=res.selector).first_or_404()
        ba = BusinessAccount.query.filter(BusinessAccount.business_id == bs.id, BusinessAccount.id == pk).first_or_404()
        return ba.delete(), 200


namespace.add_resource(BusinessAccountListResource, '/')
namespace.add_resource(BusinessAccountResource, '/<pk>')
