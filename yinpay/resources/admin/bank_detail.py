from flask_restplus import Resource, Namespace

from yinpay.ext import flask_filter, pagination, db
from yinpay.models import BankDetail
from yinpay.schema import BankDetailSchema

namespace = Namespace('BankDetails')
schema = BankDetailSchema()


class BankDetailListResource(Resource):
    def get(self):
        search = BankDetail()
        if namespace.payload:
            search = flask_filter.search(BankDetail, [namespace.payload.get('filters')], BankDetailSchema(many=True),
                                         order_by=namespace.payload.get('order_by', 'created'))
        return pagination.paginate(search, schema, marshmallow=True)

    def post(self):
        bank_detail = BankDetail()
        bank_detail = schema.load(namespace.payload, session=db.session, instance=bank_detail, unknown='exclude')
        bank_detail.save()
        return schema.dump(bank_detail), 200


class BankDetailResource(Resource):
    def get(self, pk):
        bank_detail = BankDetail.query.get_or_404(pk)
        return schema.dump(bank_detail), 200

    def put(self, pk):
        bank_detail = BankDetail.query.get_or_404(pk)
        bank_detail = schema.load(namespace.payload, session=db.session, instance=bank_detail, unknown='exclude')
        bank_detail.save()
        return bank_detail.dump(bank_detail)

    def delete(self, pk):
        bank_detail = BankDetail.query.get_or_404(pk)
        bank_detail.delete(), 200


namespace.add_resource(BankDetailListResource, '/')
namespace.add_resource(BankDetailResource, '/<pk>')
