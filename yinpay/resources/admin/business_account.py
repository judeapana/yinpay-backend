from flask_jwt_extended import jwt_required
from flask_restplus import Resource, Namespace

from yinpay.ext import flask_filter, pagination, db
from yinpay.models import BusinessAccount
from yinpay.schema import BusinessAccountSchema

namespace = Namespace('BusinessAccount', path='/ba', description='', decorators=[jwt_required()])

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
        ba = BusinessAccount.query.get_or_404(pk)
        return ba, 200

    def put(self, pk):
        ba = BusinessAccount.query.get_or_404(pk)
        ba = schema.load(namespace.payload, session=db.session, instance=ba, unknown='exclude')
        ba.save()
        return schema.dump(ba), 200

    def delete(self, pk):
        ba = BusinessAccount.query.get_or_404(pk)
        return ba.delete(), 200


namespace.add_resource(BusinessAccountListResource, '/')
namespace.add_resource(BusinessAccountResource, '/<pk>')
