from marshmallow import fields

from yinpay import ma
from yinpay.models import User, Business, BusinessAccount, PersonnelGroup, UserMeta, NextOfKin, Bank, BankDetail, Memo, \
    UserLeave, UserDoc, Department, Period, WorkingDay, DailyRate, SocialSecurityRate, DeductionGroup, EarningGroup, \
    Tax, Attendance, UserAttendance, UserDeduction, UserEarning, Queue, Setting


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        include_fk = True
        load_instance = True

    business = fields.Nested('BusinessSchema', many=True)
    user_meta = fields.Nested('UserMeta', many=False)


class BusinessSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Business
        include_fk = True
        load_instance = True

    user = fields.Nested(UserSchema, exclude=('business', 'user_meta'))
    accounts = fields.Nested('BusinessAccountSchema', many=True)
    setting = fields.Nested('SettingSchema', exclude=('business',))


class BusinessAccountSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = BusinessAccount
        include_fk = True
        load_instance = True

    business = fields.Nested(BusinessSchema, exclude=('user', 'accounts'))


class PersonnelGroupSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = PersonnelGroup
        include_fk = True
        load_instance = True

    users = fields.Nested(UserSchema, many=True, exclude=('business', 'user_meta'))
    deductions = fields.Nested('DeductionGroupSchema', many=True)
    earnings = fields.Nested('EarningGroupSchema', many=True)
    taxes = fields.Nested('TaxSchema', many=True)


class UserMetaSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = UserMeta
        include_fk = True
        load_instance = True

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
        include_fk = True
        load_instance = True

    user_meta = fields.Nested('UserMetaSchema', many=True)


class BankSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Bank
        include_fk = True
        load_instance = True

    accounts = fields.Nested('BankDetailSchema', many=True)


class BankDetailSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = BankDetail
        include_fk = True
        load_instance = True

    bank = fields.Nested(BankSchema)
    user_meta = fields.Nested(UserMetaSchema, exclude='bank_details')


class MemoSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Memo
        include_fk = True
        load_instance = True


class UserLeaveSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = UserLeave
        include_fk = True
        load_instance = True

    user_meta = fields.Nested(UserMetaSchema)


class UserDocSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = UserDoc
        include_fk = True
        load_instance = True

    user_meta = fields.Nested(UserMetaSchema)


class DepartmentSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Department
        include_fk = True
        load_instance = True

    users = fields.Nested(UserMetaSchema, exclude=('department',), many=True)


class PeriodSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Period
        include_fk = True
        load_instance = True

    working_days = fields.Nested('WorkingDaySchema', many=True)
    daily_rates = fields.Nested('DailyRateSchema', many=True)
    ssr = fields.Nested('SocialSecurityRateSchema', many=True)
    taxes = fields.Nested('TaxSchema', many=True)
    attendances = fields.Nested('AttendanceSchema', many=True)


class WorkingDaySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = WorkingDay
        include_fk = True
        load_instance = True

    period = fields.Nested(PeriodSchema, many=True)
    personnel_group = fields.Nested(PersonnelGroupSchema, many=True)


class DailyRateSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = DailyRate
        include_fk = True
        load_instance = True

    user_meta = fields.Nested(UserMetaSchema, exclude='daily_rates')


class SocialSecurityRateSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = SocialSecurityRate
        include_fk = True
        load_instance = True

    period = fields.Nested(PeriodSchema)


class DeductionGroupSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = DeductionGroup
        include_fk = True
        load_instance = True

    personnel_group = fields.Nested(PersonnelGroupSchema)
    user_deductions = fields.Nested('UserDeductionSchema', many=True)


class EarningGroupSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = EarningGroup
        include_fk = True
        load_instance = True

    personnel_group = fields.Nested(PersonnelGroupSchema)
    user_earnings = fields.Nested('UserEarningSchema', many=True)


class TaxSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Tax
        include_fk = True
        load_instance = True

    period = fields.Nested(PeriodSchema)
    personnel_group = fields.Nested(PersonnelGroupSchema)


class AttendanceSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Attendance
        include_fk = True
        load_instance = True

    period = fields.Nested(PeriodSchema)
    user_attendances = fields.Nested('UserAttendanceSchema', many=True)


class UserAttendanceSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = UserAttendance
        include_fk = True
        load_instance = True

    user_meta = fields.Nested(UserMetaSchema)
    attendance = fields.Nested(AttendanceSchema)


class UserDeductionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = UserDeduction
        include_fk = True
        load_instance = True

    user_meta = fields.Nested(UserMetaSchema)
    deduction_group = fields.Nested(DeductionGroupSchema)


class UserEarningSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = UserEarning
        include_fk = True
        load_instance = True

    user_meta = fields.Nested(UserMetaSchema)
    earning_group = fields.Nested(EarningGroupSchema)


class QueueSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Queue
        include_fk = True
        load_instance = True


class SettingSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Setting
        include_fk = True
        load_instance = True

    business = fields.Nested(BusinessSchema)
