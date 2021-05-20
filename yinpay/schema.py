from flask import request
from flask_jwt_extended import current_user
from marshmallow import fields, ValidationError, validates, validates_schema

from yinpay import ma
from yinpay.common.helpers import get_uuid
from yinpay.common.validators import tel, username, password
from yinpay.models import User, Business, BusinessAccount, PersonnelGroup, UserMeta, NextOfKin, Bank, BankDetail, Memo, \
    UserLeave, UserDoc, Department, Period, WorkingDay, DailyRate, SocialSecurityRate, DeductionGroup, EarningGroup, \
    Tax, Attendance, UserAttendance, UserDeduction, UserEarning, Queue, Setting


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        include_fk = True
        load_instance = True

    username = fields.String(required=True, validate=[username])
    phone_number = fields.String(required=True, validate=tel)
    email_address = fields.Email(required=True)
    password = fields.String(load_only=True, dump_only=False, validate=password)
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
        include_relationship = True

    @validates_schema
    def validate(self, data, **kwargs):
        errors = {}
        if request.method == 'POST':
            if current_user.business.filter_by(name=data.get('name')).first():
                errors['name'] = ['This name is already in use.']
        if request.method == 'PUT':
            b = current_user.business.filter(Business.name == data.get('name')).filter(
                Business.id != get_uuid()).first()
            if b:
                errors['name'] = ['This name is already in use.']
        if errors:
            raise ValidationError(errors)


class BusinessAccountSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = BusinessAccount
        include_fk = True
        load_instance = True

    business = fields.Nested(BusinessSchema, exclude=('user', 'accounts'))

    @validates_schema
    def validate_business_name(self):
        pass


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

    @validates_schema
    def validate_business_name(self, data, **kwargs):
        errors = {}
        business = current_user.business.filter_by(id=data.get('business_id')).first_or_404()
        if request.method == 'POST':
            if business.personnel_groups.filter_by(name=data.get('name')).first():
                errors['name'] = ['This name is already in use.']
        if request.method == 'PUT':
            b = business.personnel_groups.filter(PersonnelGroup.name == data.get('name')).filter(
                PersonnelGroup.id != get_uuid()).first()
            if b:
                errors['name'] = ['This name is already in use.']
        if errors:
            raise ValidationError(errors)


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

    @validates_schema
    def validate(self, data, **kwargs):
        errors = {}
        business = current_user.business.filter_by(id=data.get('business_id')).first_or_404()
        if request.method == 'POST':
            if business.banks.filter_by(name=data.get('name')).first():
                errors['name'] = ['This name is already in use.']
        if request.method == 'PUT':
            b = business.banks.filter(Bank.name == data.get('name')).filter(
                Bank.id != get_uuid()).first()
            if b:
                errors['name'] = ['This name is already in use.']
        if errors:
            raise ValidationError(errors)


class BankDetailSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = BankDetail
        include_fk = True
        load_instance = True

    bank = fields.Nested(BankSchema)
    user_meta = fields.Nested(UserMetaSchema, exclude=('bank_details',))

    @validates_schema
    def validate_business_user_meta(self):
        pass


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

    @validates_schema
    def validate(self, data, **kwargs):
        errors = {}
        business = current_user.business.filter_by(id=data.get('business_id')).first_or_404()
        if request.method == 'POST':
            if business.departments.filter_by(name=data.get('name')).first():
                errors['name'] = ['This name is already in use.']
        if request.method == 'PUT':
            b = business.departments.filter(Department.name == data.get('name')).filter(
                Department.id != get_uuid()).first()
            if b:
                errors['name'] = ['This name is already in use.']
        if errors:
            raise ValidationError(errors)


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

    @validates_schema
    def validate_business_name(self, data, **kwargs):
        errors = {}
        business = current_user.business.filter_by(id=data.get('business_id')).first_or_404()
        if request.method == 'POST':
            if business.periods.filter_by(name=data.get('name')).first():
                errors['name'] = ['This name is already in use.']
        if request.method == 'PUT':
            b = business.periods.filter(Period.name == data.get('name')).filter(
                Period.id != get_uuid()).first()
            if b:
                errors['name'] = ['This name is already in use.']
        if errors:
            raise ValidationError(errors)


class WorkingDaySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = WorkingDay
        include_fk = True
        load_instance = True

    period = fields.Nested(PeriodSchema, many=True)
    personnel_group = fields.Nested(PersonnelGroupSchema, many=True)

    @validates_schema
    def validate_period_personnel_group_business(self):
        pass


class DailyRateSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = DailyRate
        include_fk = True
        load_instance = True

    user_meta = fields.Nested(UserMetaSchema, exclude=('daily_rates',))

    @validates_schema
    def validate_period_business_user_meta(self):
        pass


class SocialSecurityRateSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = SocialSecurityRate
        include_fk = True
        load_instance = True

    period = fields.Nested(PeriodSchema)

    @validates_schema
    def validate_business_period(self):
        pass


class DeductionGroupSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = DeductionGroup
        include_fk = True
        load_instance = True

    personnel_group = fields.Nested(PersonnelGroupSchema)
    user_deductions = fields.Nested('UserDeductionSchema', many=True)

    @validates_schema
    def validate(self, data, **kwargs):
        errors = {}
        business = current_user.business.filter_by(id=data.get('business_id')).first_or_404()
        if request.method == 'POST':
            if business.deduction_groups.filter_by(name=data.get('name')).first():
                errors['name'] = ['This name is already in use.']
        if request.method == 'PUT':
            b = business.deduction_groups.filter(DeductionGroup.name == data.get('name')).filter(
                DeductionGroup.id != get_uuid()).first()
            if b:
                errors['name'] = ['This name is already in use.']
        if errors:
            raise ValidationError(errors)


class EarningGroupSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = EarningGroup
        include_fk = True
        load_instance = True

    personnel_group = fields.Nested(PersonnelGroupSchema)
    user_earnings = fields.Nested('UserEarningSchema', many=True)

    @validates_schema
    def validate(self, data, **kwargs):
        errors = {}
        business = current_user.business.filter_by(id=data.get('business_id')).first_or_404()
        if request.method == 'POST':
            if business.earning_groups.filter_by(name=data.get('name')).first():
                errors['name'] = ['This name is already in use.']
        if request.method == 'PUT':
            b = business.earning_groups.filter(EarningGroup.name == data.get('name')).filter(
                EarningGroup.id != get_uuid()).first()
            if b:
                errors['name'] = ['This name is already in use.']
        if errors:
            raise ValidationError(errors)


class TaxSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Tax
        include_fk = True
        load_instance = True

    period = fields.Nested(PeriodSchema)
    personnel_group = fields.Nested(PersonnelGroupSchema)

    @validates_schema()
    def validate(self, data, **kwargs):
        errors = {}
        business = current_user.business.filter_by(id=data.get('business_id')).first_or_404()
        if request.method == 'POST':
            if business.taxes.filter_by(name=data.get('name'), period_id=data.get('period_id'),
                                        personnel_group_id=data.get('personnel_group_id')).first():
                errors['name'] = ['This name is already in use.']
        if request.method == 'PUT':
            b = business.taxes.filter(Tax.name == data.get('name'), period_id=data.get('period_id'),
                                      personnel_group_id=data.get('personnel_group_id')).filter(
                Tax.id != get_uuid()).first()
            if b:
                errors['name'] = ['This name is already in use.']
        if errors:
            raise ValidationError(errors)


class AttendanceSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Attendance
        include_fk = True
        load_instance = True

    period = fields.Nested(PeriodSchema)
    user_attendances = fields.Nested('UserAttendanceSchema', many=True)

    @validates_schema
    def validate(self, data, **kwargs):
        errors = {}
        business = current_user.business.filter_by(id=data.get('business_id')).first_or_404()
        if request.method == 'POST':
            if business.attendances.filter_by(name=data.get('name')).first():
                errors['name'] = ['This name is already in use.']
        if request.method == 'PUT':
            b = business.attendances.filter(Attendance.name == data.get('name')).filter(
                Attendance.id != get_uuid()).first()
            if b:
                errors['name'] = ['This name is already in use.']
        if errors:
            raise ValidationError(errors)


class UserAttendanceSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = UserAttendance
        include_fk = True
        load_instance = True

    user_meta = fields.Nested(UserMetaSchema)
    attendance = fields.Nested(AttendanceSchema)

    @validates_schema
    def validate_user_meta_attendance(self): pass


class UserDeductionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = UserDeduction
        include_fk = True
        load_instance = True

    user_meta = fields.Nested(UserMetaSchema)
    deduction_group = fields.Nested(DeductionGroupSchema)

    @validates_schema
    def validate_deduction_group(self, data, **kwargs):
        errors = {}
        business = current_user.business.filter_by(id=data.get('business_id')).first_or_404()
        user_meta = business.user_metas.filter_by(id=data.get('user_meta_id')).first_or_404()
        if request.method == 'POST':
            if user_meta.user_deductions.filter(UserEarning.id == data.get('deduction_group_id')).first():
                errors['deduction_group'] = ['This deduction is already applied to this user']
        if request.method == 'PUT':

            if user_meta.user_deductions.filter(UserEarning.id != data.get('deduction_group_id'), ).first():
                errors['deduction_group'] = ['This deduction is already applied to this user']
        if errors:
            raise ValidationError(errors)


class UserEarningSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = UserEarning
        include_fk = True
        load_instance = True

    user_meta = fields.Nested(UserMetaSchema)
    earning_group = fields.Nested(EarningGroupSchema)

    @validates('earning_group')
    def validate_earning_group(self, data, **kwargs):
        errors = {}
        business = current_user.business.filter_by(id=data.get('business_id')).first_or_404()
        user_meta = business.user_metas.filter_by(id=data.get('user_meta_id')).first_or_404()
        if request.method == 'POST':
            if user_meta.user_earnings.filter(UserEarning.id == data.get('deduction_group_id')).first():
                errors['earning_group'] = ['This earning is already applied to this user']
        if request.method == 'PUT':

            if user_meta.user_earnings.filter(UserEarning.id != data.get('deduction_group_id'), ).first():
                errors['earning_group'] = ['This earning is already applied to this user']
        if errors:
            raise ValidationError(errors)


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


class EmailAddressSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        only = ('email_address',)

    email_address = fields.Email(required=True)


class PasswordSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        only = ('password',)

    password = fields.String(required=True, validate=password)
