from flask_jwt_extended import jwt_required, current_user
from flask_restplus import Resource, Namespace

from yinpay.common.localns import selector
from yinpay.ext import flask_filter, pagination, db
from yinpay.models import Bank
from yinpay.schema import BankSchema

namespace = Namespace('bank', description='', path='/bank', decorators=[jwt_required()])

schema = BankSchema()


class BankListResource(Resource):
    @namespace.expect(selector)
    def get(self):
        sel = selector.parse_args()
        search = current_user.business.filter_by(id=sel.selector).first_or_404().banks
        if namespace.payload:
            search = flask_filter.search(current_user.business.filter_by(id=selector).first_or_404(),
                                         [namespace.payload.get('filters')], BankSchema(many=True),
                                         order_by=namespace.payload.get('order_by', 'created'))
        return pagination.paginate(search, schema, marshmallow=True)

    @namespace.expect(selector)
    def post(self):
        sel = selector.parse_args()
        bank = Bank()
        bs = current_user.business.filter_by(id=sel.selector).first_or_404()
        namespace.payload['business_id'] = bs.id
        bank = schema.load(namespace.payload, session=db.session, instance=bank, unknown='exclude')
        bank.save()
        return schema.dump(bank), 200


class BankResource(Resource):
    @namespace.expect(selector)
    def get(self, pk):
        sel = selector.parse_args()
        bs = current_user.business.filter_by(id=sel.selector).first_or_404()
        bank = Bank.query.filter(Bank.id == pk, Bank.business_id == bs.id).first_or_404()
        return schema.dump(bank)

    @namespace.expect(selector)
    def put(self, pk):
        sel = selector.parse_args()
        bs = current_user.business.filter_by(id=sel.selector).first_or_404()
        bank = Bank.query.filter(Bank.id == pk, Bank.business_id == bs.id).first_or_404()
        namespace.payload['business_id'] = bs.id
        bank = schema.load(namespace.payload, session=db.session, instance=bank, unknown='exclude')
        bank.save()
        return schema.dump(bank), 200

    @namespace.expect(selector)
    def delete(self, pk):
        sel = selector.parse_args()
        bs = current_user.business.filter_by(id=sel.selector).first_or_404()
        bank = Bank.query.filter(Bank.id == pk, Bank.business_id == bs.id).first_or_404()
        bank.delete(), 202


namespace.add_resource(BankListResource, '/')
namespace.add_resource(BankResource, '/<pk>')
