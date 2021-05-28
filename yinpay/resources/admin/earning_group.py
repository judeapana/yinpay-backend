from flask_jwt_extended import jwt_required, current_user
from flask_restplus import Resource, Namespace

from yinpay.common.localns import selector
from yinpay.ext import flask_filter, pagination, db
from yinpay.models import EarningGroup
from yinpay.schema import EarningGroupSchema

namespace = Namespace('earning_group', path='/earning-group', decorators=[jwt_required()])
schema = EarningGroupSchema()


class EarningGroupListResource(Resource):
    def get(self):
        sel = selector.parse_args()
        search = current_user.business.filter_by(id=sel.selector).first_or_404().earning_groups
        if namespace.payload:
            search = flask_filter.search(current_user.business.filter_by(id=sel.selector).first_or_404().earning_groups,
                                         [namespace.payload.get('filters')],
                                         EarningGroupSchema(many=True),
                                         order_by=namespace.payload.get('order_by', 'created'))
        return pagination.paginate(search, schema, marshmallow=True)

    def post(self):
        sel = selector.parse_args()
        bs = current_user.business.filter_by(id=sel.selector).first_or_404()
        eg = EarningGroup()
        namespace.payload['business_id'] = bs.id
        eg = schema.load(namespace.payload, session=db.session, instance=eg, unknown='exclude')
        eg.save()
        return schema.dump(eg), 200


class EarningGroupResource(Resource):
    def get(self, pk):
        sel = selector.parse_args()
        bs = current_user.business.filter_by(id=sel.selector).first_or_404()
        eg = EarningGroup.query.filter(EarningGroup.business_id == bs.id, EarningGroup.id == pk).first_or_404()
        return schema.dump(eg), 200

    def put(self, pk):
        sel = selector.parse_args()
        bs = current_user.business.filter_by(id=sel.selector).first_or_404()
        eg = EarningGroup.query.filter(EarningGroup.business_id == bs.id, EarningGroup.id == pk).first_or_404()
        namespace.payload['business_id'] = bs.id
        eg = schema.load(namespace.payload, session=db.session, instance=eg, unknown='exclude')
        eg.save()
        return schema.dump(eg), 200

    @namespace.expect(selector)
    def delete(self, pk):
        sel = selector.parse_args()
        bs = current_user.business.filter_by(id=sel.selector).first_or_404()
        eg = EarningGroup.query.filter(EarningGroup.business_id == bs.id, EarningGroup.id == pk).first_or_404()
        return eg.delete(), 200


namespace.add_resource(EarningGroupListResource, '/')
namespace.add_resource(EarningGroupResource, '/<pk>')
