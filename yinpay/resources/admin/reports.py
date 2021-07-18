from flask import request
from flask_jwt_extended import jwt_required
from flask_restplus import Resource, Namespace
from marshmallow import fields

from yinpay import User, ma
from yinpay.common.core import PaySlip
from yinpay.common.helpers import flash
from yinpay.models import Period, UserLeave, UserAttendance, Attendance
from yinpay.schema import PayslipSchema, UserLeaveSchema, UserAttendanceSchema

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


class EarningResource(Resource):
    def get(self):
        period = Period.query.get_or_404(request.args.get('period_id'))
        payroll = []
        for user in User.query.filter(None != User.user_meta).all():
            payslip = PaySlip(user, period)
            payroll.append(payslip)
        schema = PayslipSchema(only=(
            'user', 'daily_rate', 'basic_salary', 'earnings', 'allowances', 'earning_allowances', 'total_earning_amt',
            'total_allowance_amt', 'gross_salary', 'net_pay',))
        return schema.dump(payroll, many=True), 200


class DeductionResource(Resource):
    def get(self):
        period = Period.query.get_or_404(request.args.get('period_id'))
        payroll = []
        for user in User.query.filter(None != User.user_meta).all():
            payslip = PaySlip(user, period)
            payroll.append(payslip)
        schema = PayslipSchema(only=(
            'user',
            'ssnit_emp_amt',
            'tax_deductions',
            'tax_deduction_sum',
            'tax_paye',
            'deductions',
            'total_deductions_amt',
            'total_deduction',))
        return schema.dump(payroll, many=True), 200


class SsnitResource(Resource):
    def get(self):
        period = Period.query.get_or_404(request.args.get('period_id'))
        payroll = []
        for user in User.query.filter(None != User.user_meta).all():
            payslip = PaySlip(user, period)
            payroll.append(payslip)
        schema = PayslipSchema(only=(
            'user',
            'ssnit_emp_amt',
            'ssnit_emper_amt',
            'ssnit_total_amt',
            'ssnit_tier1_amt',
            'ssnit_tier2_amt',
            'ssnit_total_tiers',
            'total_deduction',))
        return schema.dump(payroll, many=True), 200


class LeaveAttendanceSchema(ma.Schema):
    on = fields.Date('%Y-%m-%d')
    _from = fields.Date(attribute='from')
    _to = fields.Date(attribute='to')


class AttendanceResource(Resource):
    def get(self):
        schema = LeaveAttendanceSchema()
        obj = UserAttendanceSchema()
        schema = schema.load(request.args, unknown='include')
        if schema.get('on'):
            user_leave = UserAttendance.query.join(Attendance, UserAttendance.attendance_id == Attendance.id).filter(
                Attendance.day == schema.get('on')).all()
            return obj.dump(user_leave, many=True), 200
        elif schema.get('from') and schema.get('to'):
            user_leave = UserAttendance.query.join(Attendance, UserAttendance.attendance_id == Attendance.id).filter(
                Attendance.day.between(schema.get('from'), schema.get('to'))).all()
            return obj.dump(user_leave, many=True), 200
        else:
            return flash('No query parameters were found', 400)


class LeaveResource(Resource):
    def get(self):
        schema = LeaveAttendanceSchema()
        obj = UserLeaveSchema()
        schema = schema.load(request.args, unknown='include')
        if schema.get('on'):
            user_leave = UserLeave.query.filter(UserLeave.from_date == schema.get('on')).all()
            return obj.dump(user_leave, many=True)
        elif schema.get('from') and schema.get('to'):
            user_leave = UserLeave.query.filter(UserLeave.from_date.between(schema.get('from'), schema.get('to'))).all()
            return obj.dump(user_leave, many=True)
        else:
            return flash('No query parameters were found', 400)


class DashboardResource(Resource):
    def get(self):
        pass


class PayrollDashboardResource(Resource):
    def get(self):
        pass


class HrmDashboardResource(Resource):
    def get(self):
        pass


namespace.add_resource(PayslipResource, '/payslip', endpoint='payslip')
namespace.add_resource(PayrollResource, '/payroll', endpoint='payroll')
namespace.add_resource(EarningResource, '/earning', endpoint='earning')
namespace.add_resource(DeductionResource, '/deduction', endpoint='deduction')
namespace.add_resource(SsnitResource, '/ssnit', endpoint='ssnit')
namespace.add_resource(AttendanceResource, '/attendance', endpoint='attendance')
namespace.add_resource(LeaveResource, '/leave', endpoint='leave')
namespace.add_resource(DashboardResource, '/dashboard', endpoint='dashboard')
namespace.add_resource(PayrollDashboardResource, '/r-payroll', endpoint='r_payroll')
namespace.add_resource(HrmDashboardResource, '/r-hrm', endpoint='r_hrm')
