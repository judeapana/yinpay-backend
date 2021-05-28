from flask import request
from flask_jwt_extended import jwt_required, current_user
from flask_restplus import Resource, Namespace

from yinpay.common.localns import selector
from yinpay.ext import flask_filter, pagination, db
from yinpay.models import Department
from yinpay.schema import DepartmentSchema

namespace = Namespace('Department', path='/department', decorators=[jwt_required()])

schema = DepartmentSchema()


class DepartmentListResource(Resource):
    @namespace.expect(selector)
    def get(self):
        search = current_user.business.filter_by(id=request.args.get('selector')).first_or_404().departments
        if namespace.payload:
            search = flask_filter.search(
                current_user.business.filter_by(id=request.args.get('selector')).first_or_404().departments,
                [namespace.payload.get('filters')],
                DepartmentSchema(many=True),
                order_by=namespace.payload.get('order_by', 'created'))
        return pagination.paginate(search, schema, marshmallow=True)

    @namespace.expect(selector)
    def post(self):
        bs = current_user.business.filter_by(id=request.args.get('selector')).first_or_404()
        dp = Department()
        namespace.payload['business_id'] = bs.id
        dp = schema.load(namespace.payload, session=db.session, instance=dp, unknown='exclude')
        dp.save()
        return schema.dump(dp), 200


class DepartmentResource(Resource):
    @namespace.expect(selector)
    def get(self, pk):
        dp = current_user.business.filter_by(id=request.args.get('selector')).first_or_404().departments.filter_by(
            id=pk).first_or_404()
        return schema.dump(dp), 200

    @namespace.expect(selector)
    def put(self, pk):
        bs = current_user.business.filter_by(id=request.args.get('selector')).first_or_404()
        dp = Department.query.filter_by(id=pk, business_id=bs.id).first_or_404()
        namespace.payload['business_id'] = request.args.get('selector')
        dp = schema.load(namespace.payload, session=db.session, instance=dp, unknown='exclude')
        dp.save()
        return schema.dump(dp), 200

    @namespace.expect(selector)
    def delete(self, pk):
        dp = current_user.business.filter_by(id=request.args.get('selector')).first_or_404().departments.filter_by(
            id=pk).first_or_404()
        return dp.delete(), 200


namespace.add_resource(DepartmentListResource, '/')
namespace.add_resource(DepartmentResource, '/<pk>')
