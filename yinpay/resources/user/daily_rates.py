from flask_jwt_extended import current_user
from flask_restplus import Resource, Namespace

from yinpay.ext import flask_filter, pagination
from yinpay.models import DailyRate
from yinpay.schema import CurrentUserDailyRateSchema

namespace = Namespace('userDailyRate', path='/user/daily-rate')

schema = CurrentUserDailyRateSchema()


class CurUserDailyRateResourceList(Resource):
    def get(self):
        search = current_user.user_meta.daily_rates
        if namespace.payload:
            search = flask_filter.search(current_user.user_meta.daily_rates,
                                         [namespace.payload.get('filters')], CurrentUserDailyRateSchema(many=True),
                                         order_by=namespace.payload.get('order_by', 'created'))
        return pagination.paginate(search, schema, marshmallow=True)


class CurUserDailyRateResource(Resource):
    def get(self, pk):
        user_daily = current_user.user_meta.daily_rates.filter(DailyRate.id == pk).first_or_404()
        return schema.dump(user_daily), 200
