from flask import request
from marshmallow import fields, ValidationError, validates

from yinpay import ma
from yinpay.common.helpers import get_uuid
from yinpay.common.validators import tel, username
from yinpay.models import User, Business, BusinessAccount, PersonnelGroup, UserMeta, NextOfKin, Bank, BankDetail, Memo, \
    UserLeave, UserDoc, Department, Period, WorkingDay, DailyRate, SocialSecurityRate, DeductionGroup, EarningGroup, \
    Tax, Attendance, UserAttendance, UserDeduction, UserEarning, Queue, Setting


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        include_fk = True
        load_instance = True
        # include_relationship=True

    username = fields.String(required=True, validate=[username])
    phone_number = fields.String(required=True, validate=tel)
    email_address = fields.String(required=True)
    password = fields.String(load_only=True)
    first_name = fields.String(required=True)
    last_name = fields.String(required=True)
    business = fields.Nested('BusinessSchema', many=True)
    user_meta = fields.Nested('UserMetaSchema', many=False)

    @validates('username')
    def validate_username(self, value):
        if request.method == 'POST':
            user = User.query.filter_by(username=value).first()
            if user:
                raise ValidationError('Already registered to another account')
        if request.method == 'PUT':
            user = User.query.filter(User.id == get_uuid()).filter(User.username != value).first()
            if user:
                raise ValidationError('Already registered to another account')

    @validates('email_address')
    def validate_email_address(self, value):
        if request.method == 'POST':
            user = User.query.filter_by(email_address=value).first()
            if user:
                raise ValidationError('Already registered to another account')
        if request.method == 'PUT':
            user = User.query.filter(User.id == get_uuid()).filter(User.email_address != value).first()
            if user:
                raise ValidationError('Already registered to another account')


class BusinessSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Business
        include_fk = True
        load_instance = True

    user = fields.Nested(UserSchema, exclude=('business', 'user_meta'))
    accounts = fields.Nested('BusinessAccountSchema', many=True)
    setting = fields.Nested('SettingSchema', exclude=('business',))
    business_accounts = fields.Nested('BusinessAccountSchema', many=True)
    personnel_groups = fields.Nested('PersonnelGroupSchema', many=True)
    user_metas = fields.Nested('UserMetaSchema', many=True)
    next_of_kins = fields.Nested('NextOfKinSchema', many=True)
    banks = fields.Nested('BankSchema', many=True)
    bank_details = fields.Nested('BankDetailSchema', many=True)
    memos = fields.Nested('MemoSchema', many=True)
    user_leaves = fields.Nested('UserLeaveSchema', many=True)
    user_docs = fields.Nested('UserDocSchema', many=True)
    departments = fields.Nested('DepartmentSchema', many=True)
    periods = fields.Nested('PeriodSchema', many=True)
    working_days = fields.Nested('WorkingDaySchema', many=True)
    daily_rates = fields.Nested('DailyRateSchema', many=True)
    social_security_rates = fields.Nested('SocialSecurityRateSchema', many=True)
    deduction_groups = fields.Nested('DeductionGroupSchema', many=True)
    earning_groups = fields.Nested('EarningGroupSchema', many=True)
    taxes = fields.Nested('TaxSchema', many=True)
    attendances = fields.Nested('AttendanceSchema', many=True)
    user_attendances = fields.Nested('UserAttendanceSchema', many=True)
    user_deductions = fields.Nested('UserDeductionSchema', many=True)
    user_earnings = fields.Nested('UserEarningSchema', many=True)
    queues = fields.Nested('QueueSchema', many=True)

    @validates('name')
    def validate_name(self, value):
        pass


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
    working_days = fields.Nested('WorkingDaySchema', many=True)

    @validates
    def validate_name(self, value):
        pass


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

    @validates
    def validate_name(self, value):
        pass


class BankDetailSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = BankDetail
        include_fk = True
        load_instance = True

    bank = fields.Nested(BankSchema)
    user_meta = fields.Nested(UserMetaSchema, exclude=('bank_details',))


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

    @validates
    def validate_name(self, value):
        pass


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

    @validates
    def validate_name(self, value):
        pass


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

    user_meta = fields.Nested(UserMetaSchema, exclude=('daily_rates',))


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

    @validates
    def validate_name(self, value):
        pass


class EarningGroupSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = EarningGroup
        include_fk = True
        load_instance = True

    personnel_group = fields.Nested(PersonnelGroupSchema)
    user_earnings = fields.Nested('UserEarningSchema', many=True)

    @validates
    def validate_name(self, value):
        pass


class TaxSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Tax
        include_fk = True
        load_instance = True

    period = fields.Nested(PeriodSchema)
    personnel_group = fields.Nested(PersonnelGroupSchema)

    @validates
    def validate_name(self, value):
        pass


class AttendanceSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Attendance
        include_fk = True
        load_instance = True

    period = fields.Nested(PeriodSchema)
    user_attendances = fields.Nested('UserAttendanceSchema', many=True)

    @validates
    def validate_name(self, value):
        pass


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
