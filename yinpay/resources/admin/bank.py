from flask_restplus import Resource, Namespace

from yinpay import flask_filter, pagination, db
from yinpay.models import Bank
from yinpay.schema import BankSchema

namespace = Namespace('bank', description='', path='/bank')

schema = BankSchema()


class BankListResource(Resource):
    def get(self):
        search = Bank
        if namespace.payload:
            search = flask_filter.search(Bank, [namespace.payload.get('filters')], BankSchema(many=True),
                                         order_by=namespace.payload.get('order_by', 'created'))
        return pagination.paginate(search, schema, marshmallow=True)

    def post(self):
        bank = Bank()
        bank = schema.load(namespace.payload, session=db.session, instance=bank, unknown='exclude')
        bank.save()
        return schema.dump(bank), 200


class BankResource(Resource):
    def get(self, pk):
        pass

    def put(self, pk):
        pass

    def delete(self, pk):
        pass


namespace.add_resource(BankListResource, '/')
namespace.add_resource(BankResource, '/<pk>')
