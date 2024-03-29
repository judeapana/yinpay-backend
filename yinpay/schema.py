from flask import request, url_for
from flask_jwt_extended import current_user
from marshmallow import fields, ValidationError, validates, validates_schema, pre_load
from marshmallow.validate import Length

from yinpay import ma
from yinpay.common.helpers import get_uuid
from yinpay.common.validators import tel, username, password
from yinpay.models import User, Business, BusinessAccount, PersonnelGroup, UserMeta, NextOfKin, Bank, BankDetail, Memo, \
    UserLeave, UserDoc, Department, Period, WorkingDay, DailyRate, SocialSecurityRate, DeductionGroup, EarningGroup, \
    Tax, Attendance, UserAttendance, UserDeduction, UserEarning, Queue, Setting


class ProfileSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        include_fk = True
        load_instance = True
        include_relationship = True

    username = fields.String(required=True, validate=[username])
    phone_number = fields.String(required=True, validate=tel)
    email_address = fields.Email(required=True)
    first_name = fields.String(required=True)
    last_name = fields.String(required=True)

    @validates('username')
    def validate_username(self, value):
        if request.method == 'PUT':
            user = User.query.filter(User.id != current_user.id, User.username == value).first()
            if user:
                raise ValidationError('Already registered to another account')

    @validates('email_address')
    def validate_email_address(self, value):
        if request.method == 'PUT':
            user = User.query.filter(User.id != current_user.id, User.email_address == value).first()
            if user:
                raise ValidationError('Already registered to another account')


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        include_fk = True
        load_instance = True
        include_relationship = True

    username = fields.String(required=True, validate=[username])
    phone_number = fields.String(required=True, validate=tel)
    email_address = fields.Email(required=True)
    password = fields.String(load_only=True, dump_only=False, validate=password)
    first_name = fields.String(required=True)
    last_name = fields.String(required=True)
    business = fields.Nested('BusinessSchema', many=True)
    user_meta = fields.Nested('UserMetaSchema', many=False, exclude=('user', 'user_earnings', 'user_deductions'),
                              dump_only=True)

    @validates('username')
    def validate_username(self, value):
        if request.method == 'POST':
            user = User.query.filter_by(username=value).first()
            if user:
                raise ValidationError('Already registered to another account')
        if request.method == 'PUT':
            user = User.query.filter(User.id != get_uuid(), User.username == value).first()
            if user:
                raise ValidationError('Already registered to another account')

    @validates('email_address')
    def validate_email_address(self, value):
        if request.method == 'POST':
            user = User.query.filter_by(email_address=value).first()
            if user:
                raise ValidationError('Already registered to another account')
        if request.method == 'PUT':
            user = User.query.filter(User.id != get_uuid(), User.email_address == value).first()
            if user:
                raise ValidationError('Already registered to another account')


class BusinessSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Business
        include_fk = True
        load_instance = True
        include_relationship = True
        exclude = ('user_id',)

    name = fields.String(required=True, validate=[Length(3)])
    support_email = fields.Email()
    phone_number = fields.String(validate=[tel])
    logo = fields.Function(lambda x: url_for('api.protected_dir', filename=x.logo, _external=True) if x.logo else '')

    @pre_load
    def loader(self, data, **kwargs):
        data['user_id'] = current_user.id
        return data

    @validates_schema
    def validate(self, data, **kwargs):
        errors = {}
        if request.method == 'POST':
            if current_user.business.filter_by(name=data.get('name')).first():
                errors['name'] = ['This name is already in use.']
        if request.method == 'PUT':
            b = Business.query.filter(Business.user_id == current_user.id, Business.name == data.get('name'),
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

    business = fields.Nested(BusinessSchema)

    @validates_schema
    def validate_business_name(self, data, **kwargs):
        errors = {}
        business = current_user.business.filter_by(id=data.get('business_id')).first_or_404()
        if request.method == 'POST':
            if business.business_accounts.filter_by(account_name=data.get('account_name')).first():
                errors['name'] = ['This name is already in use.']
        if request.method == 'PUT':
            b = BusinessAccount.query.filter(BusinessAccount.business_id == data.get('business_id'),
                                             BusinessAccount.account_name == data.get('account_name'),
                                             BusinessAccount.id != get_uuid()).first()
            if b:
                errors['name'] = ['This name is already in use.']
        if errors:
            raise ValidationError(errors)


class PersonnelGroupSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = PersonnelGroup
        include_fk = True
        load_instance = True

    name = fields.String(validate=[Length(3)])
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
            b = PersonnelGroup.query.filter(PersonnelGroup.business_id == data.get('business_id'),
                                            PersonnelGroup.name == data.get('name'),
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
        unknown = 'include'
        include_relationship = True

    user = fields.Nested(UserSchema, only=('id', 'username', 'email_address'))
    personnel_group = fields.Nested(PersonnelGroupSchema)
    department = fields.Nested('DepartmentSchema')
    next_of_kins = fields.Nested('NextOfKinSchema', many=True)
    bank_details = fields.Nested('BankDetailSchema', many=True)
    leaves = fields.Nested('UserLeaveSchema', many=True)
    docs = fields.Nested('UserDocSchema', many=True)
    daily_rates = fields.Nested('DailyRateSchema', many=True)
    attendances = fields.Nested('AttendanceSchema', many=True)
    user_deductions = fields.Nested('UserDeductionSchema', many=True)
    user_earnings = fields.Nested('UserEarningSchema', many=True)


#

class NextOfKinSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = NextOfKin
        include_fk = True
        load_instance = True

    dob = fields.Date('%Y-%m-%d')
    user_meta = fields.Nested('UserMetaSchema', many=False, only=('user',))


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
            b = Bank.query.filter(Bank.business_id == data.get('business_id'), Bank.name == data.get('name'),
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

    bank = fields.Nested(BankSchema, exclude=('accounts',))
    user_meta = fields.Nested(UserMetaSchema, exclude=('bank_details',))

    @validates_schema
    def validate_business_user_meta(self, data, **kwargs):
        errors = {}
        business = current_user.business.filter_by(id=data.get('business_id')).first_or_404()
        if request.method == 'POST':
            if business.bank_details.filter_by(user_meta_id=data.get('user_meta_id'),
                                               bank_id=data.get('bank_id'), disabled=False).first():
                errors['user_meta_id'] = ['This user can\'t have more than one active account']
        if request.method == 'PUT':
            b = BankDetail.query.filter(BankDetail.business_id == business.id, BankDetail.id != get_uuid(),
                                        BankDetail.disabled == False,
                                        BankDetail.user_meta_id == data.get('user_meta_id'),
                                        BankDetail.bank_id == data.get('bank_id'),
                                        ).first()
            if b:
                errors['user_meta_id'] = ['This user can\'t have more than one active account']
        if errors:
            raise ValidationError(errors)


class MemoSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Memo
        include_fk = True
        load_instance = True

    date = fields.Date('%Y-%m-%d')


class UserLeaveSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = UserLeave
        include_fk = True
        load_instance = True

    from_date = fields.Date('%Y-%m-%d')
    to_date = fields.Date('%Y-%m-%d')

    user_meta = fields.Nested(UserMetaSchema, only=('user',))


class UserDocSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = UserDoc
        include_fk = True
        load_instance = True

    doc = fields.Function(lambda x: url_for('api.protected_dir', filename=x.doc, _external=True) if x.doc else '')
    user_meta = fields.Nested(UserMetaSchema, only=('user',))
    date = fields.Date('%Y-%m-%d')


class DepartmentSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Department
        include_fk = True
        load_instance = True

    name = fields.String(required=True)
    users = fields.Nested(UserMetaSchema, exclude=('department',), many=True)

    @validates_schema
    def validate(self, data, **kwargs):
        errors = {}
        business = current_user.business.filter_by(id=data.get('business_id')).first_or_404()
        if request.method == 'POST':
            if business.departments.filter_by(name=data.get('name')).first():
                errors['name'] = ['This name is already in use.']
        if request.method == 'PUT':
            current_user.business.filter_by(id=data.get('business_id')).first_or_404()
            b = Department.query.filter(Department.business_id == data.get('business_id'),
                                        Department.name == data.get('name'), Department.id != get_uuid()).first()
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
    month = fields.Date('%Y-%m')

    @validates_schema
    def validate_business_name(self, data, **kwargs):
        errors = {}
        business = current_user.business.filter_by(id=data.get('business_id')).first_or_404()
        if request.method == 'POST':
            if business.periods.filter_by(name=data.get('name')).first():
                errors['name'] = ['This name is already in use.']
        if request.method == 'PUT':
            b = Period.query.filter(Period.business_id == data.get('business_id'),
                                    Period.name == data.get('name'),
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

    period = fields.Nested(PeriodSchema, many=False, only=('id', 'name', 'month', 'make_payment',))
    personnel_group = fields.Nested(PersonnelGroupSchema, many=False, only=('name', 'category',))

    @validates_schema
    def validate_period_personnel_group_business(self, data, **kwargs):
        errors = {}
        business = current_user.business.filter_by(id=data.get('business_id')).first_or_404()
        if request.method == 'POST':
            if business.working_days.filter_by(period_id=data.get('period_id'),
                                               personnel_group_id=data.get('personnel_group_id')).first():
                errors['personnel_group_id'] = ['Working days already exists for this personnel group']
        if request.method == 'PUT':
            b = WorkingDay.query.filter(WorkingDay.business_id == data.get('business_id'),
                                        WorkingDay.period_id == data.get('period_id'),
                                        WorkingDay.personnel_group_id == data.get('personnel_group_id'),
                                        WorkingDay.id != get_uuid()).first()
            if b:
                errors['personnel_group_id'] = ['Working days already exists for this personnel group']
        if errors:
            raise ValidationError(errors)


class DailyRateSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = DailyRate
        include_fk = True
        load_instance = True

    user_meta = fields.Nested(UserMetaSchema, only=('user',))
    period = fields.Nested(PeriodSchema, only=('name',))

    @validates_schema
    def validate_period_business_user_meta(self, data, **kwargs):
        errors = {}
        business = current_user.business.filter_by(id=data.get('business_id')).first_or_404()
        if request.method == 'POST':
            if business.daily_rates.filter_by(period_id=data.get('period_id'),
                                              user_meta_id=data.get('user_meta_id')).first():
                errors['period_id'] = ['This daily rate already exists for this user']
        if request.method == 'PUT':
            b = DailyRate.query.filter(DailyRate.business_id == data.get('business_id'),
                                       DailyRate.period_id == data.get('period_id'),
                                       DailyRate.id != get_uuid()).first()
            if b:
                errors['period_id'] = ['This daily rate already exists for this user']
        if errors:
            raise ValidationError(errors)


class SocialSecurityRateSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = SocialSecurityRate
        include_fk = True
        load_instance = True

    period = fields.Nested(PeriodSchema, only=('name',))

    @validates_schema
    def validate_business_period(self, data, **kwargs):
        errors = {}
        business = current_user.business.filter_by(id=data.get('business_id')).first_or_404()
        if request.method == 'POST':
            if business.social_security_rates.filter_by(period_id=data.get('period_id')).first():
                errors['period_id'] = ['This period already has a valid social security rate']
        if request.method == 'PUT':
            b = SocialSecurityRate.query.filter(SocialSecurityRate.business_id == data.get('business_id'),
                                                SocialSecurityRate.period_id == data.get('period_id'),
                                                SocialSecurityRate.id != get_uuid()).first()
            if b:
                errors['period_id'] = ['This period already has a valid social security rate']
        if errors:
            raise ValidationError(errors)


class DeductionGroupSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = DeductionGroup
        include_fk = True
        load_instance = True

    personnel_group = fields.Nested(PersonnelGroupSchema, only=('id', 'name',))
    user_deductions = fields.Nested('UserDeductionSchema', many=True, only=('user_meta.user',))

    @validates_schema
    def validate(self, data, **kwargs):
        errors = {}
        business = current_user.business.filter_by(id=data.get('business_id')).first_or_404()
        if request.method == 'POST':
            if business.deduction_groups.filter_by(name=data.get('name')).first():
                errors['name'] = ['This name is already in use.']
        if request.method == 'PUT':
            b = DeductionGroup.query.filter(DeductionGroup.business_id == data.get('business_id'),
                                            DeductionGroup.name == data.get('name'),
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

    personnel_group = fields.Nested(PersonnelGroupSchema, only=('id', 'name',))
    user_earnings = fields.Nested('UserEarningSchema', many=True, only=('user_meta.user',))

    @validates_schema
    def validate(self, data, **kwargs):
        errors = {}
        business = current_user.business.filter_by(id=data.get('business_id')).first_or_404()
        if request.method == 'POST':
            if not business.personnel_groups.filter_by(id=data.get('personnel_group_id')).first():
                errors['personnel_group_id'] = ['Personnel group doesn\'t belong to this business']
            if business.earning_groups.filter_by(name=data.get('name')).first():
                errors['name'] = ['This name is already in use.']
        if request.method == 'PUT':
            b = EarningGroup.query.filter(EarningGroup.business_id == data.get('business_id'),
                                          EarningGroup.name == data.get('name'),
                                          EarningGroup.id != get_uuid()).first()
            if b:
                errors['name'] = ['This name is already in use.']
            if not Business.query.filter(Business.id == data.get('business_id'),
                                         Business.personnel_groups.any(id=data.get('personnel_group_id'))).first():
                errors['personnel_group_id'] = ['Personnel group doesn\'t belong to this business']
        if errors:
            raise ValidationError(errors)


class TaxSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Tax
        include_fk = True
        load_instance = True

    period = fields.Nested(PeriodSchema, only=('name', 'id'))
    personnel_group = fields.Nested(PersonnelGroupSchema, only=('name', 'id'))

    @validates_schema()
    def validate(self, data, **kwargs):
        errors = {}
        business = current_user.business.filter_by(id=data.get('business_id')).first_or_404()
        if request.method == 'POST':
            if business.taxes.filter_by(name=data.get('name'), period_id=data.get('period_id'),
                                        personnel_group_id=data.get('personnel_group_id')).first():
                errors['name'] = ['This name is already in use.']
        if request.method == 'PUT':
            b = Tax.query.filter(Tax.business_id == data.get('business_id'), Tax.name == data.get('name'),
                                 Tax.period_id == data.get('period_id'),
                                 Tax.personnel_group_id == data.get('personnel_group_id'),
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

    period = fields.Nested(PeriodSchema, exclude=('attendances',))
    user_attendances = fields.Nested('UserAttendanceSchema', many=True)
    day = fields.Date("%Y-%m-%d")

    @validates_schema
    def validate(self, data, **kwargs):
        errors = {}
        business = current_user.business.filter_by(id=data.get('business_id')).first_or_404()
        if request.method == 'POST':
            if business.attendances.filter_by(name=data.get('name')).first():
                errors['name'] = ['This name is already in use. or dat']
        if request.method == 'PUT':
            b = Attendance.query.filter(Attendance.business_id == data.get('business_id'),
                                        Attendance.name == data.get('name'), Attendance.id != get_uuid()).first()
            if b:
                errors['name'] = ['This name is already in use.']
        if errors:
            raise ValidationError(errors)


class UserAttendanceSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = UserAttendance
        include_fk = True
        load_instance = True

    user_meta = fields.Nested(UserMetaSchema, only=('user', 'id'))
    attendance = fields.Nested(AttendanceSchema, only=('name', 'id'))

    @validates_schema
    def validate_user_meta_attendance(self, data, **kwargs):
        errors = {}
        business = current_user.business.filter_by(id=data.get('business_id')).first_or_404()
        if request.method == 'POST':

            if business.user_attendances.filter(UserAttendance.attendance_id == data.get('attendance_id'),
                                                UserAttendance.user_meta_id == data.get('user_meta_id'),
                                                UserAttendance.time == data.get('time')).first():
                errors['time'] = ['Time already exist for this user']
        if request.method == 'PUT':

            if UserAttendance.query.filter(UserAttendance.time == data.get('time'),
                                           UserAttendance.business_id == data.get('business_id'),
                                           UserAttendance.id != get_uuid(),
                                           UserAttendance.user_meta_id == data.get('user_meta_id')).first():
                errors['time'] = ['Time already exist for this user']
        if errors:
            raise ValidationError(errors)


class UserDeductionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = UserDeduction
        include_fk = True
        load_instance = True

    user_meta = fields.Nested(UserMetaSchema, dump_only=True, exclude=('user_deductions', 'user_earnings'))
    deduction_group = fields.Nested(DeductionGroupSchema, exclude=('user_deductions',))
    period = fields.Nested(PeriodSchema, only=('name',))

    @validates_schema
    def validate_deduction_group(self, data, **kwargs):
        errors = {}
        business = current_user.business.filter_by(id=data.get('business_id')).first_or_404()
        user_meta = business.user_metas.filter_by(id=data.get('user_meta_id')).first_or_404()
        if request.method == 'POST':
            if user_meta.user_deductions.filter(UserDeduction.period_id == data.get('period_id'),
                                                UserDeduction.deduction_group_id == data.get(
                                                    'deduction_group_id')).first():
                errors['deduction_group_id'] = ['This deduction is already applied to this user']
        if request.method == 'PUT':

            if UserDeduction.query.filter(UserDeduction.id != get_uuid(),
                                          UserDeduction.user_meta.has(id=data.get('user_meta_id')),
                                          UserDeduction.period_id == data.get('period.id'),
                                          UserDeduction.business_id == data.get('business_id'), ).first():
                errors['deduction_group_id'] = ['This deduction is already applied to this user']
        if errors:
            raise ValidationError(errors)


class UserEarningSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = UserEarning
        include_fk = True
        load_instance = True

    user_meta = fields.Nested(UserMetaSchema, dump_only=True, exclude=('user_earnings', 'user_deductions'))
    earning_group = fields.Nested(EarningGroupSchema, exclude=('user_earnings',))
    period = fields.Nested(PeriodSchema, only=('name',))

    @validates_schema
    def validate_earning_group(self, data, **kwargs):
        errors = {}
        business = current_user.business.filter_by(id=data.get('business_id')).first_or_404()
        user_meta = business.user_metas.filter_by(id=data.get('user_meta_id')).first_or_404()
        if request.method == 'POST':
            if user_meta.user_earnings.filter(UserDeduction.period_id == data.get('period_id'),
                                              UserEarning.earning_group_id == data.get('earning_group_id')).first():
                errors['earning_group_id'] = ['This earning is already applied to this user']
        if request.method == 'PUT':

            if UserEarning.query.filter(UserEarning.business_id == data.get('business_id'),
                                        UserDeduction.user_meta.has(id=data.get('user_meta_id')),
                                        UserDeduction.period_id == data.get('period.id'),
                                        UserEarning.id != get_uuid(),
                                        UserEarning.earning_group_id != data.get('earning_group_id'), ).first():
                errors['earning_group_id'] = ['This earning is already applied to this user']
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
        include_relationship = True


class EmailAddressSchema(ma.SQLAlchemyAutoSchema):
    email_address = fields.Email(required=True)


class PasswordSchema(ma.SQLAlchemyAutoSchema):
    password = fields.String(required=True, validate=password)


class CurrentUserAttendanceSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Attendance


class CurrentUserDailyRateSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = DailyRate


class CurrentUserDeductionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = UserDeduction


class CurrentUserEarningSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = UserEarning


class CurrentUserDocSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = UserDoc


class CurrentUserLeaveSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = UserLeave


class CurUserNextKinSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = NextOfKin


class PayslipSchema(ma.Schema):
    user = fields.Nested(UserSchema, many=False,
                         only=('user_meta.user', 'user_meta.title', 'first_name', 'last_name','email_address','phone_number','img'
                               ))
    absence = fields.Integer()
    excused = fields.Integer()
    present = fields.Integer()
    working_days = fields.Nested(WorkingDaySchema, many=False, only=('days', 'hours', 'disabled', 'notes'))
    without_pay_leave = fields.Integer()
    with_pay_leave = fields.Integer()
    days_worked = fields.Integer()
    daily_rate = fields.Nested(DailyRateSchema, many=False,
                               only=('main_amount', 'emergency_amount', 'disabled', 'notes'))

    basic_salary = fields.Float()
    hourly_rate = fields.Float()
    earnings = fields.List(fields.Dict())
    allowances = fields.List(fields.Dict())
    earning_allowances = fields.List(fields.Dict())
    total_earning_amt = fields.Float()
    total_allowance_amt = fields.Float()
    gross_salary = fields.Float()
    ssnit_rates = fields.Nested(SocialSecurityRateSchema, many=False, only=('emp_rate', 'emper_rate', 'tier1','tier2'))
    ssnit_emp_amt = fields.Float()
    ssnit_emper_amt = fields.Float()
    ssnit_total_amt = fields.Float()
    ssnit_tier1_amt = fields.Float()
    ssnit_tier2_amt = fields.Float()
    ssnit_total_tiers = fields.Float()
    taxable_income = fields.Float()
    tax_deductions = fields.List(fields.Dict())
    tax_deduction_sum = fields.Float()
    tax_paye = fields.Float()
    deductions = fields.List(fields.Dict())
    total_deductions_amt = fields.Float()
    total_deduction = fields.Float()
    net_pay = fields.Float()
