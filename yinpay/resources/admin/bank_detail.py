from flask_jwt_extended import jwt_required, current_user
from flask_restplus import Resource, Namespace

from yinpay.common.localns import selector
from yinpay.ext import flask_filter, pagination, db
from yinpay.models import BankDetail
from yinpay.schema import BankDetailSchema

namespace = Namespace('BankDetails', description='', path='/bank-detail', decorators=[jwt_required()])
schema = BankDetailSchema()


class BankDetailListResource(Resource):
    @namespace.expect(selector)
    def get(self):
        sel = selector.parse_args()
        search = current_user.business.filter_by(id=sel.selector).first_or_404().bank_details
        if namespace.payload:
            search = flask_filter.search(current_user.business.filter_by(id=sel.selector).first_or_404().bank_details,
                                         [namespace.payload.get('filters')], BankDetailSchema(many=True),
                                         order_by=namespace.payload.get('order_by', 'created'))
        return pagination.paginate(search, schema, marshmallow=True)

    @namespace.expect(selector)
    def post(self):
        sel = selector.parse_args()
        bs = current_user.business.filter_by(id=sel.selector).first_or_404()
        bank_detail = BankDetail()
        namespace.payload['business_id'] = bs.id
        bank_detail = schema.load(namespace.payload, session=db.session, instance=bank_detail, unknown='exclude')
        bank_detail.save()
        return schema.dump(bank_detail), 200


class BankDetailResource(Resource):
    @namespace.expect(selector)
    def get(self, pk):
        sel = selector.parse_args()
        bs = current_user.business.filter_by(id=sel.selector).first_or_404()
        bank_detail = BankDetail.query.filter(BankDetail.id == pk, BankDetail.business_id == bs.id).first_or_404()
        return schema.dump(bank_detail), 200

    @namespace.expect(selector)
    def put(self, pk):
        sel = selector.parse_args()
        bs = current_user.business.filter_by(id=sel.selector).first_or_404()
        bank_detail = BankDetail.query.filter(BankDetail.id == pk, BankDetail.business_id == bs.id).first_or_404()
        namespace.payload['business_id'] = bs.id
        bank_detail = schema.load(namespace.payload, session=db.session, instance=bank_detail, unknown='exclude')
        bank_detail.save()
        return schema.dump(bank_detail)

    @namespace.expect(selector)
    def delete(self, pk):
        sel = selector.parse_args()
        bs = current_user.business.filter_by(id=sel.selector).first_or_404()
        bank_detail = BankDetail.query.filter(BankDetail.id == pk, BankDetail.business_id == bs.id).first_or_404()
        bank_detail.delete(), 200


namespace.add_resource(BankDetailListResource, '/')
namespace.add_resource(BankDetailResource, '/<pk>')
