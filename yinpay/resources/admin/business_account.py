from flask_restplus import Resource, Namespace

from yinpay import flask_filter, pagination, db
from yinpay.models import BusinessAccount
from yinpay.schema import BusinessAccountSchema

namespace = Namespace('BusinessAccount', path='/ba')

schema = BusinessAccountSchema()


class BusinessAccountListResource(Resource):
    def get(self):
        search = BusinessAccount
        if namespace.payload:
            search = flask_filter.search(BusinessAccount, [namespace.payload.get('filters')],
                                         BusinessAccountSchema(many=True),
                                         order_by=namespace.payload.get('order_by', 'created'))
        return pagination.paginate(search, schema, marshmallow=True)

    def post(self):
        ba = BusinessAccount()
        ba = schema.load(namespace.payload, session=db.session, instance=ba, unknown='exclude')
        ba.save()
        return schema.dump(ba), 200


class BusinessAccountResource(Resource):
    def get(self, pk):
        pass

    def put(self, pk):
        pass

    def delete(self, pk):
        pass


namespace.add_resource(BusinessAccountListResource, '/')
namespace.add_resource(BusinessAccountResource, '/<pk>')
