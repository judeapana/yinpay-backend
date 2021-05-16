from flask_restplus import Resource, Namespace

from yinpay import flask_filter, pagination, db
from yinpay.models import EarningGroup
from yinpay.schema import EarningGroupSchema

namespace = Namespace('earning_group', path='/earning-group')
schema = EarningGroupSchema()


class EarningGroupListResource(Resource):
    def get(self):
        search = EarningGroup
        if namespace.payload:
            search = flask_filter.search(EarningGroup, [namespace.payload.get('filters')],
                                         EarningGroupSchema(many=True),
                                         order_by=namespace.payload.get('order_by', 'created'))
        return pagination.paginate(search, schema, marshmallow=True)

    def post(self):
        eg = EarningGroup()
        eg = schema.load(namespace.payload, session=db.session, instance=eg, unknown='exclude')
        eg.save()
        return schema.dump(eg), 200


class EarningGroupResource(Resource):
    def get(self, pk):
        pass

    def put(self, pk):
        pass

    def delete(self, pk):
        pass


namespace.add_resource(EarningGroupListResource, '/')
namespace.add_resource(EarningGroupResource, '/<pk>')
