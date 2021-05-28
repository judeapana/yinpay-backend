from flask_jwt_extended import jwt_required, current_user
from flask_restplus import Resource, Namespace

from yinpay import flask_filter, pagination, db
from yinpay.common.localns import selector
from yinpay.models import UserEarning
from yinpay.schema import UserEarningSchema

namespace = Namespace('user_earning', path='/user-earning', decorators=[jwt_required()])

schema = UserEarningSchema()


class UserEarningListResource(Resource):
    @namespace.expect(selector)
    def get(self):
        sel = selector.parse_args()
        search = current_user.business.filter_by(id=sel.selector).first_or_404().user_earnings
        if namespace.payload:
            search = flask_filter.search(current_user.business.filter_by(id=sel.selector).first_or_404().user_earnings,
                                         [namespace.payload.get('filters')], UserEarningSchema(many=True),
                                         order_by=namespace.payload.get('order_by', 'created'))
        return pagination.paginate(search, schema, marshmallow=True)

    @namespace.expect(selector)
    def post(self):
        sel = selector.parse_args()
        bs = current_user.business.filter_by(id=sel.selector).first_or_404()
        user_earning = UserEarning()
        namespace.payload['business_id'] = bs.id
        user_earning = schema.load(namespace.payload, session=db.session, instance=user_earning, unknown='exclude')
        user_earning.save()
        return schema.dump(user_earning), 200


class UserEarningResource(Resource):
    @namespace.expect(selector)
    def get(self, pk):
        sel = selector.parse_args()
        bs = current_user.business.filter_by(id=sel.selector).first_or_404()
        user_earning = UserEarning.query.filter(UserEarning.business_id == bs.id, UserEarning.id == pk).first_or_404()
        return schema.dump(user_earning), 200

    @namespace.expect(selector)
    def put(self, pk):
        sel = selector.parse_args()
        bs = current_user.business.filter_by(id=sel.selector).first_or_404()
        user_earning = UserEarning.query.filter(UserEarning.business_id == bs.id, UserEarning.id == pk).first_or_404()
        namespace.payload['business_id'] = bs.id
        user_earning = schema.load(namespace.payload, session=db.session, instance=user_earning, unknown='exclude')
        user_earning.save()
        return schema.dump(user_earning), 200

    @namespace.expect(selector)
    def delete(self, pk):
        sel = selector.parse_args()
        bs = current_user.business.filter_by(id=sel.selector).first_or_404()
        user_earning = UserEarning.query.filter(UserEarning.business_id == bs.id, UserEarning.id == pk).first_or_404()
        return user_earning.delete(), 200


namespace.add_resource(UserEarningListResource, '/')
namespace.add_resource(UserEarningResource, '/<pk>')
