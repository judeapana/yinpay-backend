from flask_restplus import Resource, Namespace

from yinpay import flask_filter, pagination, db
from yinpay.models import DeductionGroup
from yinpay.schema import DeductionGroupSchema

namespace = Namespace('deduction_group', path='/deduction-group')

schema = DeductionGroupSchema()


class DeductionGroupListResource(Resource):
    def get(self):
        search = DeductionGroup
        if namespace.payload:
            search = flask_filter.search(DeductionGroup, [namespace.payload.get('filters')],
                                         DeductionGroupSchema(many=True),
                                         order_by=namespace.payload.get('order_by', 'created'))
        return pagination.paginate(search, schema, marshmallow=True)

    def post(self):
        dg = DeductionGroup()
        dg = schema.load(namespace.payload, session=db.session, instance=dg, unknown='exclude')
        dg.save()
        return schema.dump(dg), 200


class DeductionGroupResource(Resource):
    def get(self, pk):
        pass

    def put(self, pk):
        pass

    def delete(self, pk):
        pass


namespace.add_resource(DeductionGroupListResource, '/')
namespace.add_resource(DeductionGroupResource, '/<pk>')
