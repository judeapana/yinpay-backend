from marshmallow import fields

from yinpay import ma
from yinpay.models import User, Business, BusinessAccount, PersonnelGroup, UserMeta, NextOfKin, Bank, BankDetail, Memo, \
    UserLeave, UserDoc, Department, Period, WorkingDay, DailyRate, SocialSecurityRate, DeductionGroup, EarningGroup, \
    Tax, Attendance, UserAttendance, UserDeduction, UserEarning, Queue, Setting


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User

    business = fields.Nested('BusinessSchema', many=True)
    user_meta = fields.Nested('UserMeta', many=False)


class BusinessSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Business

    user = fields.Nested(UserSchema, exclude=('business', 'user_meta'))
    accounts = fields.Nested('BusinessAccountSchema', many=True)
    setting = fields.Nested('SettingSchema', exclude=('business',))


class BusinessAccountSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = BusinessAccount

    business = fields.Nested(BusinessSchema, exclude=('user', 'accounts'))


class PersonnelGroupSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = PersonnelGroup

    users = fields.Nested(UserSchema, many=True, exclude=('business', 'user_meta'))
    deductions = fields.Nested('DeductionGroupSchema', many=True)
    earnings = fields.Nested('EarningGroupSchema', many=True)
    taxes = fields.Nested('TaxSchema', many=True)


class UserMetaSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = UserMeta

    personnel_group = fields.Nested(PersonnelGroupSchema)
    department = fields.Nested('DepartmentSchema')
    next_of_kins = fields.Nested('NextOfKinSchema', many=True)
    bank_details = fields.Nested('BankDetailSchema', many=True)
    leaves = fields.Nested('UserLeaveSchema', many=True)
    docs = fields.Nested('UserDoc', many=True)
    working_days = fields.Nested('WorkingDaySchema', many=True)
    daily_rates = fields.Nested('DailyRateSchema', many=True)
    attendances = fields.Nested('AttendanceSchema', many=True)


class NextOfKinSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = NextOfKin

    user_meta = fields.Nested('UserMetaSchema', many=True)


class BankSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Bank

    accounts = fields.Nested('BankDetailSchema', many=True)


class BankDetailSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = BankDetail

    bank = fields.Nested(BankSchema)
    user_meta = fields.Nested(UserMetaSchema, exclude='bank_details')


class MemoSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Memo


class UserLeaveSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = UserLeave

    user_meta = fields.Nested(UserMetaSchema)


class UserDocSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = UserDoc

    user_meta = fields.Nested(UserMetaSchema)


class DepartmentSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Department

    users = fields.Nested(UserMetaSchema, exclude=('department',), many=True)


class PeriodSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Period

    working_days = fields.Nested('WorkingDaySchema', many=True)
    daily_rates = fields.Nested('DailyRateSchema', many=True)
    ssr = fields.Nested('SocialSecurityRateSchema', many=True)
    taxes = fields.Nested('TaxSchema', many=True)
    attendances = fields.Nested('AttendanceSchema', many=True)


class WorkingDaySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = WorkingDay

    period = fields.Nested(PeriodSchema, many=True)
    personnel_group = fields.Nested(PersonnelGroupSchema, many=True)


class DailyRateSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = DailyRate

    user_meta = fields.Nested(UserMetaSchema, exclude='daily_rates')


class SocialSecurityRateSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = SocialSecurityRate

    period = fields.Nested(PeriodSchema)


class DeductionGroupSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = DeductionGroup

    personnel_group = fields.Nested(PersonnelGroupSchema)
    user_deductions = fields.Nested('UserDeductionSchema', many=True)


class EarningGroupSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = EarningGroup

    personnel_group = fields.Nested(PersonnelGroupSchema)
    user_earnings = fields.Nested('UserEarningSchema', many=True)


class TaxSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Tax

    period = fields.Nested(PeriodSchema)
    personnel_group = fields.Nested(PersonnelGroupSchema)


class AttendanceSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Attendance

    period = fields.Nested(PeriodSchema)
    user_attendances = fields.Nested('UserAttendanceSchema', many=True)


class UserAttendanceSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = UserAttendance

    user_meta = fields.Nested(UserMetaSchema)
    attendance = fields.Nested(AttendanceSchema)


class UserDeductionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = UserDeduction

    user_meta = fields.Nested(UserMetaSchema)
    deduction_group = fields.Nested(DeductionGroupSchema)


class UserEarningSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = UserEarning

    user_meta = fields.Nested(UserMetaSchema)
    earning_group = fields.Nested(EarningGroupSchema)


class QueueSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Queue


class SettingSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Setting

    business = fields.Nested(BusinessSchema)
