from flask_restplus import Resource, Namespace

from yinpay import flask_filter, pagination, db
from yinpay.models import Department
from yinpay.schema import DepartmentSchema

namespace = Namespace('Department', path='department')

schema = DepartmentSchema()


class DepartmentListResource(Resource):
    def get(self):
        search = Department
        if namespace.payload:
            search = flask_filter.search(Department, [namespace.payload.get('filters')], DepartmentSchema(many=True),
                                         order_by=namespace.payload.get('order_by', 'created'))
        return pagination.paginate(search, schema, marshmallow=True)

    def post(self):
        dg = Department()
        dg = schema.load(namespace.payload, session=db.session, instance=dg, unknown='exclude')
        dg.save()
        return schema.dump(dg), 200


class DepartmentResource(Resource):
    def get(self, pk):
        pass

    def put(self, pk):
        pass

    def delete(self, pk):
        pass


namespace.add_resource(DepartmentListResource, '/')
namespace.add_resource(DepartmentResource, '/<pk>')
