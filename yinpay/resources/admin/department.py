from flask_jwt_extended import jwt_required
from flask_restplus import Resource, Namespace

from yinpay.ext import flask_filter, pagination, db
from yinpay.models import Department
from yinpay.schema import DepartmentSchema

namespace = Namespace('Department', path='department',decorators=[jwt_required()])

schema = DepartmentSchema()


class DepartmentListResource(Resource):
    def get(self):
        search = Department
        if namespace.payload:
            search = flask_filter.search(Department, [namespace.payload.get('filters')], DepartmentSchema(many=True),
                                         order_by=namespace.payload.get('order_by', 'created'))
        return pagination.paginate(search, schema, marshmallow=True)

    def post(self):
        dp = Department()
        dp = schema.load(namespace.payload, session=db.session, instance=dp, unknown='exclude')
        dp.save()
        return schema.dump(dp), 200


class DepartmentResource(Resource):
    def get(self, pk):
        dp = Department.query.get_or_404(pk)
        return dp, 200

    def put(self, pk):
        dp = Department.query.get_or_404(pk)
        dp = schema.load(namespace.payload, session=db.session, instance=dp, unknown='exclude')
        dp.save()
        return schema.dump(dp), 200

    def delete(self, pk):
        dp = Department.query.get_or_404(pk)
        return dp.delete(), 200


namespace.add_resource(DepartmentListResource, '/')
namespace.add_resource(DepartmentResource, '/<pk>')
