from flask_jwt_extended import jwt_required, current_user
from flask_restplus import Resource, Namespace

from yinpay import flask_filter, pagination, db
from yinpay.common.localns import selector
from yinpay.models import UserDeduction
from yinpay.schema import UserDeductionSchema

namespace = Namespace('user_deduction', path='/user-deduction', decorators=[jwt_required()])

schema = UserDeductionSchema()


class UserDeductionListResource(Resource):
    @namespace.expect(selector)
    def get(self):
        sel = selector.parse_args()
        search = current_user.business.filter_by(id=sel.selector).first_or_404().user_deductions
        if namespace.payload:
            search = flask_filter.search(current_user.business.filter_by(id=sel.selector).first_or_404().user_deductions,
                                         [namespace.payload.get('filters')],
                                         UserDeductionSchema(many=True),
                                         order_by=namespace.payload.get('order_by', 'created'))
        return pagination.paginate(search, schema, marshmallow=True)

    @namespace.expect(selector)
    def post(self):
        sel = selector.parse_args()
        bs = current_user.business.filter_by(id=sel.selector).first_or_404()
        ug = UserDeduction()
        namespace.payload['business_id'] = bs.id
        ug = schema.load(namespace.payload, session=db.session, instance=ug, unknown='exclude')
        ug.save()
        return schema.dump(ug), 200


class UserDeductionResource(Resource):
    @namespace.expect(selector)
    def get(self, pk):
        sel = selector.parse_args()
        bs = current_user.business.filter_by(id=sel.selector).first_or_404()
        ug = UserDeduction.query.filter(UserDeduction.business_id == bs.id, UserDeduction.id == pk).first_or_404()
        return schema.dump(ug), 200

    @namespace.expect(selector)
    def put(self, pk):
        sel = selector.parse_args()
        bs = current_user.business.filter_by(id=sel.selector).first_or_404()
        ug = UserDeduction.query.filter(UserDeduction.business_id == bs.id, UserDeduction.id == pk).first_or_404()
        namespace.payload['business_id'] = bs.id
        ug = schema.load(namespace.payload, session=db.session, instance=ug, unknown='exclude')
        ug.save()
        return schema.dump(ug), 200

    @namespace.expect(selector)
    def delete(self, pk):
        sel = selector.parse_args()
        bs = current_user.business.filter_by(id=sel.selector).first_or_404()
        ug = UserDeduction.query.filter(UserDeduction.business_id == bs.id, UserDeduction.id == pk).first_or_404()
        return ug.delete(), 200


namespace.add_resource(UserDeductionListResource, '/')
namespace.add_resource(UserDeductionResource, '/<pk>')
