from flask_jwt_extended import current_user
from flask_restplus import Resource, Namespace

from yinpay.ext import flask_filter, pagination
from yinpay.models import UserEarning
from yinpay.schema import CurrentUserEarningSchema

namespace = Namespace('userEarning', path='/user/earnings')

schema = CurrentUserEarningSchema()


class UserEarningResourceList(Resource):
    def get(self):
        search = current_user.user_meta.user_earnings
        if namespace.payload:
            search = flask_filter.search(current_user.user_meta.user_deductions,
                                         [namespace.payload.get('filters')], CurrentUserEarningSchema(many=True),
                                         order_by=namespace.payload.get('order_by', 'created'))
        return pagination.paginate(search, schema, marshmallow=True)


class UserEarningResource(Resource):
    def get(self, pk):
        earnings = current_user.user_meta.user_earnings.filter(UserEarning.id == pk).first_or_404()
        return schema.dump(earnings), 200
