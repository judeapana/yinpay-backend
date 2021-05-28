from flask_jwt_extended import jwt_required, current_user
from flask_restplus import Resource, Namespace

from yinpay.common.localns import selector
from yinpay.ext import flask_filter, pagination, db
from yinpay.models import DeductionGroup
from yinpay.schema import DeductionGroupSchema

namespace = Namespace('deduction_group', path='/deduction-group', decorators=[jwt_required()])

schema = DeductionGroupSchema()


class DeductionGroupListResource(Resource):
    @namespace.expect(selector)
    def get(self):
        sel = selector.parse_args()
        search = current_user.business.filter_by(id=sel.selector).first_or_404().deduction_groups
        if namespace.payload:
            search = flask_filter.search(
                current_user.business.filter_by(id=sel.selector).first_or_404().deduction_groups,
                [namespace.payload.get('filters')],
                DeductionGroupSchema(many=True),
                order_by=namespace.payload.get('order_by', 'created'))
        return pagination.paginate(search, schema, marshmallow=True)

    @namespace.expect(selector)
    def post(self):
        sel = selector.parse_args()
        bs = current_user.business.filter_by(id=sel.selector).first_or_404()
        dg = DeductionGroup()
        namespace.payload['business_id'] = bs.id
        dg = schema.load(namespace.payload, session=db.session, instance=dg, unknown='exclude')
        dg.save()
        return schema.dump(dg), 200


class DeductionGroupResource(Resource):
    @namespace.expect(selector)
    def get(self, pk):
        sel = selector.parse_args()
        bs = current_user.business.filter_by(id=sel.selector).first_or_404()
        dg = DeductionGroup.query.filter(DeductionGroup.business_id == bs.id, DeductionGroup.id == pk).first_or_404()
        return schema.dump(dg), 200

    @namespace.expect(selector)
    def put(self, pk):
        sel = selector.parse_args()
        bs = current_user.business.filter_by(id=sel.selector).first_or_404()
        dg = DeductionGroup.query.filter(DeductionGroup.business_id == bs.id, DeductionGroup.id == pk).first_or_404()
        namespace.payload['business_id'] = bs.id
        dg = schema.load(namespace.payload, session=db.session, instance=dg, unknown='exclude')
        dg.save()
        return schema.dump(dg), 200

    @namespace.expect(selector)
    def delete(self, pk):
        sel = selector.parse_args()
        bs = current_user.business.filter_by(id=sel.selector).first_or_404()
        dg = DeductionGroup.query.filter(DeductionGroup.business_id == bs.id, DeductionGroup.id == pk).first_or_404()
        return dg.delete(), 200


namespace.add_resource(DeductionGroupListResource, '/')
namespace.add_resource(DeductionGroupResource, '/<pk>')
