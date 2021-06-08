import moneyed

from yinpay import User
from yinpay.models import Period


class CoreException(Exception):
    def __init__(self, message):
        Exception.__init__(self, message)


class PaySlip:
    def __init__(self, personnel: User, period: Period):
        self.psl = personnel
        self.period = period
        if not isinstance(self.psl, User):
            raise CoreException('Must be instance of a User Class')
        if not isinstance(self.period, Period):
            raise CoreException('Must be instance of a Period Class')

    @property
    def user(self):
        return self.psl

    @property
    def absence(self):
        return len(list(filter(lambda x: x.attype == 'Absent' and x.attendance.period_id == self.period.id,
                               self.psl.user_meta.attendances.all())))

    @property
    def excused(self):
        return len(list(filter(lambda x: x.attype == 'Excused Duty' and x.attendance.period_id == self.period.id,
                               self.psl.user_meta.attendances.all())))

    @property
    def present(self):
        return len(list(filter(lambda x: x.attype == 'Present' and x.attendance.period_id == self.period.id,
                               self.psl.user_meta.attendances.all())))

    @property
    def working_days(self):
        return next(
            filter(lambda x: x.period_id == self.period.id and x.disabled == False,
                   self.psl.user_meta.personnel_group.working_days.all()),
            None)

    @property
    def without_pay_leave(self):
        return len(list(filter(lambda x: x.without_pay == False and (x.from_date < self.period.month < x.to_date),
                               self.psl.user_meta.leaves.all())))

    # @property
    # def leave_attendance(self):
    #     pass

    @property
    def with_pay_leave(self):
        return len(list(filter(lambda x: x.without_pay == True and (x.from_date < self.period.month < x.to_date),
                               self.psl.user_meta.leaves.all())))

    @property
    def days_worked(self):
        return len(list(filter(lambda x: x.attype == 'Present' and x.attendance.period_id == self.period.id,
                               self.psl.user_meta.attendances.all())))

    @property
    def daily_rate(self):
        try:
            return [i for i in self.psl.user_meta.daily_rates.all() if i.period_id == self.period.id][0]
        except Exception:
            pass

    @property
    def basic_salary(self):
        try:
            if not self.daily_rate.disabled:
                if self.daily_rate.emergency_amount:
                    return self.daily_rate.emergency_amount * self.days_worked
                return self.daily_rate.main_amount * self.days_worked
            return 0
        except Exception:
            return 0

    @property
    def hourly_rate(self):
        try:
            if not self.daily_rate.disabled:
                if self.daily_rate.emergency_amount:
                    return self.daily_rate.emergency_amount / self.working_days.hours
                return self.daily_rate.main_amount / self.working_days.hours
            return 0
        except Exception:
            return 0

    @property
    def earnings(self):
        data = []
        for user_earnings in [i for i in self.psl.user_meta.user_earnings.all() if i.period_id == self.period.id]:
            if not user_earnings.earning_group.allowance:
                if user_earnings.earning_group.per_day:
                    value = user_earnings.rate * self.days_worked
                else:
                    value = user_earnings.rate
                data.append({user_earnings.earning_group.name: value})
        return data

    @property
    def allowances(self):
        data = []
        for user_earnings in [i for i in self.psl.user_meta.user_earnings.all() if i.period_id == self.period.id]:
            if user_earnings.earning_group.allowance:
                if user_earnings.earning_group.per_day:
                    value = user_earnings.rate * self.days_worked
                else:
                    value = user_earnings.rate
                data.append({user_earnings.earning_group.name: value})
        return data

    @property
    def earning_allowances(self):
        data = []
        for earnings in [i for i in self.psl.user_meta.user_earnings.all() if i.period_id == self.period.id]:
            value = earnings.rate
            data.append({earnings.earning_group.name: value})
        return data

    @property
    def total_earning_amt(self):
        data = []
        for earnings in [i for i in self.psl.user_meta.user_earnings.all() if i.period_id == self.period.id]:
            if not earnings.earning_group.allowance:
                value = earnings.rate
                data.append(value)
        return sum(data)

    @property
    def total_allowance_amt(self):
        data = []
        for earnings in [i for i in self.psl.user_meta.user_earnings.all() if i.period_id == self.period.id]:
            if earnings.earning_group.allowance:
                value = earnings.rate
                data.append(value)
        return sum(data)

    @property
    def gross_salary(self):
        return self.basic_salary + self.total_earning_amt + self.total_allowance_amt

    # deduction
    @property
    def ssnit_rates(self):
        try:
            return self.period.ssr.first()
        except Exception:
            pass

    @property
    def ssnit_emp_amt(self):
        if self.psl.user_meta.ssn:
            if self.ssnit_rates:
                return (self.ssnit_rates.emp_rate / 100) * self.basic_salary
            else:
                return 0 * self.basic_salary
        else:
            return 0 * self.basic_salary

    @property
    def ssnit_emper_amt(self):
        if self.psl.user_meta.ssn:
            if self.ssnit_rates:
                return (self.ssnit_rates.emper_rate / 100) * self.basic_salary
            else:
                return 0 * self.basic_salary
        else:
            return 0 * self.basic_salary

    @property
    def ssnit_total_amt(self):
        return self.ssnit_emp_amt + self.ssnit_emper_amt

    @property
    def ssnit_tier1_amt(self):
        if self.psl.user_meta.ssn:
            return self.basic_salary * (self.ssnit_rates.tier1 / 100)
        else:
            return 0 * self.basic_salary

    @property
    def ssnit_tier2_amt(self):
        if self.psl.user_meta.ssn:
            return self.basic_salary * (self.ssnit_rates.tier2 / 100)
        else:
            return 0 * self.basic_salary

    @property
    def ssnit_total_tiers(self):
        return self.ssnit_tier1_amt + self.ssnit_tier2_amt

    @property
    def taxable_income(self):
        return self.basic_salary - self.ssnit_emp_amt + self.total_allowance_amt

    @property
    def tax_paye_value(self):
        try:
            return [i for i in self.psl.personnel_group.taxes.all() if
                    i.period_id == self.period.id and i.name == 'Tax Paye'][0]
        except Exception:
            pass

    @property
    def tax_paye(self):
        if self.tax_paye_value:
            if self.tax_paye_value.automate:
                return self.tax_paye_cal(self.taxable_income)
            return self.basic_salary * (self.tax_paye_value.rate / 100)
        else:
            return 0

    @property
    def deductions(self):
        data = []
        for deduction in [i for i in self.psl.user_meta.user_deductions.all() if i.period_id == self.period.id]:
            value = deduction.rate
            data.append({deduction.deduction_group.name: value})
        return data

    @property
    def total_deductions_amt(self):
        data = []
        for deduction in [i for i in self.psl.user_meta.user_deductions.all() if i.period_id == self.period.id]:
            value = deduction.rate
            data.append(value)
        return sum(data)

    @property
    def total_deduction(self):
        return self.ssnit_emp_amt + self.total_deductions_amt + self.tax_paye

    @property
    def net_pay(self):
        return self.gross_salary - self.total_deduction

    def tax_paye_cal(self, taxable_income, _moneyed=moneyed.Money, currency='GHS'):
        if taxable_income >= _moneyed(20000, currency):
            return _moneyed(4657.25, currency) + (taxable_income - _moneyed(20000, currency)) * 0.3
        elif taxable_income >= _moneyed(3539, currency):
            return _moneyed(542, currency) + (taxable_income - _moneyed(3539, currency)) * 0.25
        elif taxable_income >= _moneyed(539, currency):
            return _moneyed(17, currency) + (taxable_income - _moneyed(539, currency)) * 0.175
        elif taxable_income >= _moneyed(419, currency):
            return _moneyed(5, currency) + (taxable_income - _moneyed(419, currency)) * 0.1
        elif taxable_income >= _moneyed(319, currency):
            return (taxable_income - _moneyed(319, currency)) * 0.05
        elif taxable_income <= _moneyed(319, currency):
            return _moneyed(0, currency)
