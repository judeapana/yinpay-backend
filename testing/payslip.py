import unittest

import flask_unittest

from yinpay import create_app
from yinpay.common.core import PaySlip
from yinpay.models import User, Period
from yinpay.schema import PayslipSchema


class PaySlipTestCase(flask_unittest.ClientTestCase):
    app = create_app()

    def test_payslip(self, client):
        with self.app.app_context():
            user = User.query.filter(User.user_meta.has(id='014c7589-7ee7-4e86-83ef-82c23bb320c3')).first()
            period = Period.query.first()
            payslip = PaySlip(user, period)
            # print(payslip.absence)
            # print(payslip.excused)
            # print(payslip.present)
            # print(payslip.working_days)
            # print(payslip.without_pay_leave)
            # print(payslip.with_pay_leave)
            # print(payslip.days_worked)
            # print(payslip.daily_rate)
            # print(payslip.basic_salary)
            # print(payslip.hourly_rate)
            # print(payslip.earnings)
            # print(payslip.allowances)
            # print(payslip.earning_allowances)
            # print(payslip.total_earning_amt)
            # print(payslip.total_allowance_amt)
            # print(payslip.gross_salary)
            # print(payslip.ssnit_rates)
            # print(payslip.ssnit_emp_amt)
            # print(payslip.ssnit_emper_amt)
            # print(payslip.ssnit_total_amt)
            # print(payslip.ssnit_tier1_amt)
            # print(payslip.ssnit_tier2_amt)
            # print(payslip.ssnit_total_tiers)
            # print(payslip.taxable_income)
            # print(payslip.tax_paye_value)
            # print(payslip.tax_paye)
            # print(payslip.deductions)
            # print(payslip.total_deductions_amt)
            # print(payslip.total_deduction)
            # print(payslip.net_pay)
            schema = PayslipSchema()
            print(schema.dump(payslip))

        pass


if __name__ == "__main__":
    unittest.main()
