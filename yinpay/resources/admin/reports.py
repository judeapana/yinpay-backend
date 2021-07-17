from flask import request
from flask_jwt_extended import jwt_required
from flask_restplus import Resource, Namespace

from yinpay import User
from yinpay.common.core import PaySlip
from yinpay.models import Period
from yinpay.schema import PayslipSchema

namespace = Namespace('reports', path='/reports', decorators=[jwt_required()])


class PayslipResource(Resource):
    def get(self):
        user = User.query.filter(User.user_meta.has(id=request.args.get('user_meta_id'))).first_or_404()
        period = Period.query.get_or_404(request.args.get('period_id'))
        payslip = PaySlip(user, period)
        schema = PayslipSchema()
        return schema.dump(payslip), 200


class PayrollResource(Resource):
    def get(self):
        period = Period.query.get_or_404(request.args.get('period_id'))
        payroll = []
        for user in User.query.filter(None != User.user_meta).all():
            payslip = PaySlip(user, period)
            payroll.append(payslip)
        schema = PayslipSchema()
        return schema.dump(payroll, many=True), 200


namespace.add_resource(PayslipResource, '/payslip', endpoint='payslip')
namespace.add_resource(PayrollResource, '/payroll', endpoint='payroll')
