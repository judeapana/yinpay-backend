from flask_restplus import Resource, Namespace

from yinpay import flask_filter, pagination, db
from yinpay.models import Tax
from yinpay.schema import TaxSchema

namespace = Namespace('tax', path='/tax')
schema = TaxSchema()


class TaxListResource(Resource):
    def get(self):
        search = Tax
        if namespace.payload:
            search = flask_filter.search(Tax, [namespace.payload.get('filters')], TaxSchema(many=True),
                                         order_by=namespace.payload.get('order_by', 'created'))
        return pagination.paginate(search, schema, marshmallow=True)

    def post(self):
        tax = Tax()
        tax = schema.load(namespace.payload, session=db.session, instance=tax, unknown='exclude')
        tax.save()
        return schema.dump(tax), 200


class TaxResource(Resource):
    def get(self, pk):
        tax = Tax.query.get_or_404(pk)
        return tax, 200

    def put(self, pk):
        tax = Tax.query.get_or_404(pk)
        tax = schema.load(namespace.payload, session=db.session, instance=tax, unknown='exclude')
        tax.save()
        return schema.dump(tax), 200

    def delete(self, pk):
        tax = Tax.query.get_or_404(pk)
        return tax.delete(), 200


namespace.add_resource(TaxListResource, '/')
namespace.add_resource(TaxResource, '/<pk>')
