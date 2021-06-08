from flask_jwt_extended import current_user
from flask_restplus import Resource, Namespace

from yinpay import flask_filter, pagination
from yinpay.models import UserDeduction
from yinpay.schema import CurrentUserDeductionSchema

namespace = Namespace('userDeductions', path='/user/deduction')

schema = CurrentUserDeductionSchema()


class CurUserDeductionResourceList(Resource):
    def get(self):
        search = current_user.user_meta.user_deductions
        if namespace.payload:
            search = flask_filter.search(current_user.user_meta.user_deductions,
                                         [namespace.payload.get('filters')], CurrentUserDeductionSchema(many=True),
                                         order_by=namespace.payload.get('order_by', 'created'))
        return pagination.paginate(search, schema, marshmallow=True)


class CurUserDeductionResource(Resource):
    def get(self, pk):
        deduction = current_user.user_meta.user_deductions.filter(UserDeduction.id == pk).first_or_404()
        return schema.dump(deduction), 200
