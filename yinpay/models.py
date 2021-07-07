from uuid import uuid4

from flask import current_app
from itsdangerous import TimedJSONWebSignatureSerializer, BadSignature

from yinpay.common import Record
from yinpay.ext import db, bcrypt


class User(db.Model, Record):
    id = db.Column(db.String(100), primary_key=True, nullable=False, unique=True, default=lambda: str(uuid4()))
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=True)
    first_name = db.Column(db.String(50), nullable=True)
    last_name = db.Column(db.String(50), nullable=True)
    email_address = db.Column(db.String(50), nullable=False, unique=True)
    phone_number = db.Column(db.String(100), nullable=True)
    img = db.Column(db.String(50), nullable=True)
    disabled = db.Column(db.Boolean, default=True)
    role = db.Column(db.Enum('ADMIN', 'USER'), default='USER')
    superuser = db.Column(db.Boolean, default=False)
    hrm_support = db.Column(db.Boolean, default=False)
    payroll_support = db.Column(db.Boolean, default=False)
    last_logged_in = db.Column(db.DateTime)
    notes = db.Column(db.Text)
    business = db.relationship('Business', backref=db.backref('user'), cascade='all,delete,delete-orphan',
                               lazy='dynamic')
    user_meta = db.relationship('UserMeta', backref=db.backref('user'), cascade='all,delete,delete-orphan',
                                lazy='subquery', uselist=False)

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password)

    def create_token(self, payload=None, expires=5000):
        if payload is None:
            payload = {}
        jst = TimedJSONWebSignatureSerializer(secret_key=current_app.secret_key, expires_in=expires)
        data = {'id': str(self.id)}
        data.update(payload)
        return jst.dumps(data).decode()

    @staticmethod
    def authenticate_token(token):
        try:
            jst = TimedJSONWebSignatureSerializer(secret_key=current_app.secret_key)
            return jst.loads(token)
        except BadSignature:
            return None


class Business(db.Model, Record):
    id = db.Column(db.String(100), primary_key=True, nullable=False, unique=True, default=lambda: str(uuid4()))
    user_id = db.Column(db.String(100), db.ForeignKey('user.id', ondelete='cascade'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.Text, nullable=False)
    support_email = db.Column(db.String(50), nullable=False)
    phone_number = db.Column(db.String(50), nullable=False)
    logo = db.Column(db.String(100), nullable=True)
    btype = db.Column(db.Enum('Nonprofit Organization', 'Sole Proprietorship', 'Partnership', 'Corporation',
                              'Limited Liability Company'),
                      nullable=False)
    description = db.Column(db.Text, nullable=False)
    business_accounts = db.relationship('BusinessAccount', backref=db.backref('business'),
                                        cascade='all,delete,delete-orphan',
                                        lazy='dynamic')
    setting = db.relationship('Setting', backref=db.backref('business'), cascade='all,delete', lazy=True, uselist=False)
    personnel_groups = db.relationship('PersonnelGroup', backref=db.backref('business'), cascade='all,delete',
                                       lazy='dynamic')
    user_metas = db.relationship('UserMeta', backref=db.backref('business'), cascade='all,delete,delete-orphan',
                                 lazy='dynamic')
    next_of_kins = db.relationship('NextOfKin', backref=db.backref('business'), cascade='all,delete',
                                   lazy='dynamic')
    banks = db.relationship('Bank', backref=db.backref('business'), cascade='all,delete,delete-orphan',
                            lazy='dynamic')
    bank_details = db.relationship('BankDetail', backref=db.backref('business'), cascade='all,delete,delete-orphan',
                                   lazy='dynamic')
    memos = db.relationship('Memo', backref=db.backref('business'), cascade='all,delete',
                            lazy='dynamic')
    user_leaves = db.relationship('UserLeave', backref=db.backref('business'), cascade='all,delete',
                                  lazy='dynamic')
    user_docs = db.relationship('UserDoc', backref=db.backref('business'), cascade='all,delete',
                                lazy='dynamic')
    departments = db.relationship('Department', backref=db.backref('business'), cascade='all,delete',
                                  lazy='dynamic')
    periods = db.relationship('Period', backref=db.backref('business'), cascade='all,delete',
                              lazy='dynamic')
    working_days = db.relationship('WorkingDay', backref=db.backref('business'), cascade='all,delete',
                                   lazy='dynamic')
    daily_rates = db.relationship('DailyRate', backref=db.backref('business'), cascade='all,delete',
                                  lazy='dynamic')
    social_security_rates = db.relationship('SocialSecurityRate', backref=db.backref('business'), cascade='all,delete',
                                            lazy='dynamic')
    deduction_groups = db.relationship('DeductionGroup', backref=db.backref('business'), cascade='all,delete',
                                       lazy='dynamic')
    earning_groups = db.relationship('EarningGroup', backref=db.backref('business'), cascade='all,delete',
                                     lazy='dynamic')
    taxes = db.relationship('Tax', backref=db.backref('business'), cascade='all,delete',
                            lazy='dynamic')
    attendances = db.relationship('Attendance', backref=db.backref('business'), cascade='all,delete',
                                  lazy='dynamic')
    user_attendances = db.relationship('UserAttendance', backref=db.backref('business'), cascade='all,delete',
                                       lazy='dynamic')
    user_deductions = db.relationship('UserDeduction', backref=db.backref('business'), cascade='all,delete',
                                      lazy='dynamic')
    user_earnings = db.relationship('UserEarning', backref=db.backref('business'), cascade='all,delete',
                                    lazy='dynamic')
    queues = db.relationship('Queue', backref=db.backref('business'), cascade='all,delete',
                             lazy='dynamic')


class BusinessAccount(db.Model, Record):
    id = db.Column(db.String(100), primary_key=True, nullable=False, unique=True, default=lambda: str(uuid4()))
    business_id = db.Column(db.String(100), db.ForeignKey('business.id', ondelete='cascade'), nullable=False)
    # name = db.Column(db.String(50), nullable=False)
    account_type = db.Column(db.Enum('Bank Account', 'Mobile Money'))
    account_number = db.Column(db.String(50), nullable=False)
    code = db.Column(db.String(50), nullable=False)
    account_name = db.Column(db.String(50), nullable=False)
    currency = db.Column(db.String(50), nullable=False)
    primary = db.Column(db.Boolean, default=True)


class PersonnelGroup(db.Model, Record):
    id = db.Column(db.String(100), primary_key=True, nullable=False, unique=True, default=lambda: str(uuid4()))
    business_id = db.Column(db.String(100), db.ForeignKey('business.id', ondelete='cascade'), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    category = db.Column(db.Enum('FullTime', 'PartTime', 'Intern', 'Contract'))
    disabled = db.Column(db.Boolean, default=False)
    users = db.relationship('UserMeta', backref=db.backref('personnel_group'), cascade='all,delete,delete-orphan',
                            lazy='dynamic')
    deductions = db.relationship('DeductionGroup', backref=db.backref('personnel_group'),
                                 cascade='all,delete,delete-orphan',
                                 lazy='dynamic')
    earnings = db.relationship('EarningGroup', backref=db.backref('personnel_group'),
                               cascade='all,delete,delete-orphan',
                               lazy='dynamic')
    taxes = db.relationship('Tax', backref=db.backref('personnel_group'), cascade='all,delete,delete-orphan',
                            lazy='dynamic')
    working_days = db.relationship('WorkingDay', backref=db.backref('personnel_group'),
                                   cascade='all,delete,delete-orphan',
                                   lazy='dynamic')


class UserMeta(db.Model, Record):
    id = db.Column(db.String(100), primary_key=True, nullable=False, unique=True, default=lambda: str(uuid4()))
    business_id = db.Column(db.String(100), db.ForeignKey('business.id', ondelete='cascade'), nullable=False)
    user_id = db.Column(db.String(100), db.ForeignKey('user.id', ondelete='cascade'), nullable=False)
    personnel_group_id = db.Column(db.String(100), db.ForeignKey('personnel_group.id', ondelete='cascade'),
                                   nullable=True)
    department_id = db.Column(db.String(100), db.ForeignKey('department.id', ondelete='cascade'), nullable=True)
    title = db.Column(db.Enum('MRS', 'MISS', 'MR', 'MS'), nullable=True)
    marital_status = db.Column(db.Enum('Married', 'Divorced', 'Widowed', 'Single'), nullable=True)
    gender = db.Column(db.Enum('Male', 'Female'), nullable=True)
    religion = db.Column(db.String(50), nullable=True)
    retired = db.Column(db.Boolean, default=False)
    resigned = db.Column(db.Boolean, default=False)
    dob = db.Column(db.Date)
    addr = db.Column(db.Text, nullable=True)
    ssn = db.Column(db.String(50), nullable=True)
    tin = db.Column(db.String(50), nullable=True)
    next_of_kins = db.relationship('NextOfKin', backref=db.backref('user_meta'), cascade='all,delete,delete-orphan',
                                   lazy='dynamic')
    bank_details = db.relationship('BankDetail', backref=db.backref('user_meta'), cascade='all,delete,delete-orphan',
                                   lazy='dynamic')
    leaves = db.relationship('UserLeave', backref=db.backref('user_meta'), cascade='all,delete,delete-orphan',
                             lazy='dynamic')
    docs = db.relationship('UserDoc', backref=db.backref('user_meta'), cascade='all,delete,delete-orphan',
                           lazy='dynamic')
    daily_rates = db.relationship('DailyRate', backref=db.backref('user_meta'), cascade='all,delete,delete-orphan',
                                  lazy='dynamic')
    attendances = db.relationship('UserAttendance', backref=db.backref('user_meta'), cascade='all,delete,delete-orphan',
                                  lazy='dynamic')

    user_deductions = db.relationship('UserDeduction', backref=db.backref('user_meta'),
                                      cascade='all,delete,delete-orphan',
                                      lazy='dynamic')
    user_earnings = db.relationship('UserEarning', backref=db.backref('user_meta'), cascade='all,delete,delete-orphan',
                                    lazy='dynamic')


class NextOfKin(db.Model, Record):
    id = db.Column(db.String(100), primary_key=True, nullable=False, unique=True, default=lambda: str(uuid4()))
    business_id = db.Column(db.String(100), db.ForeignKey('business.id', ondelete='cascade'), nullable=False)
    user_meta_id = db.Column(db.String(100), db.ForeignKey('user_meta.id', ondelete='cascade'), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    middle_name = db.Column(db.String(50), nullable=False)
    dob = db.Column(db.Date, nullable=False)


class Bank(db.Model, Record):
    id = db.Column(db.String(100), primary_key=True, nullable=False, unique=True, default=lambda: str(uuid4()))
    business_id = db.Column(db.String(100), db.ForeignKey('business.id', ondelete='cascade'), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    notes = db.Column(db.Text, nullable=False)
    disabled = db.Column(db.Boolean, default=False)
    accounts = db.relationship('BankDetail', backref=db.backref('bank'), cascade='all,delete,delete-orphan',
                               lazy='dynamic')


class BankDetail(db.Model, Record):
    id = db.Column(db.String(100), primary_key=True, nullable=False, unique=True, default=lambda: str(uuid4()))
    bank_id = db.Column(db.String(100), db.ForeignKey('bank.id', ondelete='cascade'), nullable=False)
    business_id = db.Column(db.String(100), db.ForeignKey('business.id', ondelete='cascade'), nullable=False)
    user_meta_id = db.Column(db.String(100), db.ForeignKey('user_meta.id', ondelete='cascade'), nullable=False)
    no = db.Column(db.String(50), nullable=False)
    branch = db.Column(db.String(100), nullable=False)
    disabled = db.Column(db.Boolean, default=False)
    currency = db.Column(db.String(50), nullable=False)


class Memo(db.Model, Record):
    id = db.Column(db.String(100), primary_key=True, nullable=False, unique=True, default=lambda: str(uuid4()))
    business_id = db.Column(db.String(100), db.ForeignKey('business.id', ondelete='cascade'), nullable=False)
    title = db.Column(db.String(50), nullable=False)
    date = db.Column(db.DateTime)
    text = db.Column(db.Text, nullable=False)


class UserLeave(db.Model, Record):
    id = db.Column(db.String(100), primary_key=True, nullable=False, unique=True, default=lambda: str(uuid4()))
    user_meta_id = db.Column(db.String(100), db.ForeignKey('user_meta.id', ondelete='cascade'), nullable=False)
    business_id = db.Column(db.String(100), db.ForeignKey('business.id', ondelete='cascade'), nullable=False)
    without_pay = db.Column(db.Boolean, default=False)
    ltype = db.Column(db.String(50), nullable=False)
    from_date = db.Column(db.Date, nullable=False)
    to_date = db.Column(db.Date, nullable=False)
    reason = db.Column(db.Text, nullable=False)
    status = db.Column(db.Boolean, default=False)
    # we calc the from date and to day and prevent any leave to be entered within those periods


class UserDoc(db.Model, Record):
    id = db.Column(db.String(100), primary_key=True, nullable=False, unique=True, default=lambda: str(uuid4()))
    business_id = db.Column(db.String(100), db.ForeignKey('business.id', ondelete='cascade'), nullable=False)
    user_meta_id = db.Column(db.String(100), db.ForeignKey('user_meta.id', ondelete='cascade'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    notes = db.Column(db.Text, nullable=False)
    doc = db.Column(db.String(100), nullable=True)


class Department(db.Model, Record):
    id = db.Column(db.String(100), primary_key=True, nullable=False, unique=True, default=lambda: str(uuid4()))
    business_id = db.Column(db.String(100), db.ForeignKey('business.id', ondelete='cascade'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    abbr = db.Column(db.String(100), nullable=True)
    disabled = db.Column(db.Boolean, default=False)
    notes = db.Column(db.Text, nullable=True)
    user = db.relationship('UserMeta', backref=db.backref('department'), cascade='all,delete,delete-orphan',
                           lazy='dynamic')


class Period(db.Model, Record):
    id = db.Column(db.String(100), primary_key=True, nullable=False, unique=True, default=lambda: str(uuid4()))
    business_id = db.Column(db.String(100), db.ForeignKey('business.id', ondelete='cascade'), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    month = db.Column(db.Date, nullable=False)
    make_payment = db.Column(db.Boolean, default=False)
    disabled = db.Column(db.Boolean, default=False)
    notes = db.Column(db.Text, nullable=False)
    working_days = db.relationship('WorkingDay', backref=db.backref('period'), cascade='all,delete,delete-orphan',
                                   lazy='dynamic')
    daily_rates = db.relationship('DailyRate', backref=db.backref('period'), cascade='all,delete,delete-orphan',
                                  lazy='dynamic')

    ssr = db.relationship('SocialSecurityRate', backref=db.backref('period'), cascade='all,delete,delete-orphan',
                          lazy='dynamic')
    taxes = db.relationship('Tax', backref=db.backref('period'), cascade='all,delete,delete-orphan',
                            lazy='dynamic')
    attendances = db.relationship('Attendance', backref=db.backref('period'), cascade='all,delete,delete-orphan',
                                  lazy='dynamic')
    user_earnings = db.relationship('UserEarning', backref=db.backref('period'), cascade='all,delete,delete-orphan',
                                    lazy='dynamic')
    user_deduction = db.relationship('UserDeduction', backref=db.backref('period'), cascade='all,delete,delete-orphan',
                                     lazy='dynamic')


class WorkingDay(db.Model, Record):
    id = db.Column(db.String(100), primary_key=True, nullable=False, unique=True, default=lambda: str(uuid4()))
    period_id = db.Column(db.String(100), db.ForeignKey('period.id', ondelete='cascade'), nullable=False)
    business_id = db.Column(db.String(100), db.ForeignKey('business.id', ondelete='cascade'), nullable=False)
    personnel_group_id = db.Column(db.String(100), db.ForeignKey('personnel_group.id', ondelete='cascade'),
                                   nullable=False)
    days = db.Column(db.Integer, nullable=False)
    hours = db.Column(db.Integer, nullable=False)
    disabled = db.Column(db.Boolean, default=False)
    notes = db.Column(db.Text, nullable=False)


class DailyRate(db.Model, Record):
    id = db.Column(db.String(100), primary_key=True, nullable=False, unique=True, default=lambda: str(uuid4()))
    period_id = db.Column(db.String(100), db.ForeignKey('period.id', ondelete='cascade'), nullable=False)
    business_id = db.Column(db.String(100), db.ForeignKey('business.id', ondelete='cascade'), nullable=False)
    user_meta_id = db.Column(db.String(100), db.ForeignKey('user_meta.id', ondelete='cascade'), nullable=False)
    main_amount = db.Column(db.Numeric(10, 2, asdecimal=False), nullable=False)
    emergency_amount = db.Column(db.Numeric(10, 2, asdecimal=False), nullable=True)
    disabled = db.Column(db.Boolean, default=False)
    notes = db.Column(db.Text, nullable=False)


class SocialSecurityRate(db.Model, Record):
    id = db.Column(db.String(100), primary_key=True, nullable=False, unique=True, default=lambda: str(uuid4()))
    business_id = db.Column(db.String(100), db.ForeignKey('business.id', ondelete='cascade'), nullable=False)
    period_id = db.Column(db.String(100), db.ForeignKey('period.id', ondelete='cascade'), nullable=False)
    emp_rate = db.Column(db.Float, nullable=False)
    emper_rate = db.Column(db.Float, nullable=False)
    tier1 = db.Column(db.Float, nullable=False)
    tier2 = db.Column(db.Float, nullable=False)


class DeductionGroup(db.Model, Record):
    id = db.Column(db.String(100), primary_key=True, nullable=False, unique=True, default=lambda: str(uuid4()))
    business_id = db.Column(db.String(100), db.ForeignKey('business.id', ondelete='cascade'), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    personnel_group_id = db.Column(db.String(100), db.ForeignKey('personnel_group.id', ondelete='cascade'),
                                   nullable=False)
    # amount = db.Column(db.Numeric(10, 2, asdecimal=False))
    disabled = db.Column(db.Boolean, default=False)
    notes = db.Column(db.Text, nullable=False)
    per_day = db.Column(db.Boolean, default=False)
    user_deductions = db.relationship('UserDeduction', backref=db.backref('deduction_group'),
                                      cascade='all,delete,delete-orphan',
                                      lazy='dynamic')


class EarningGroup(db.Model, Record):
    id = db.Column(db.String(100), primary_key=True, nullable=False, unique=True, default=lambda: str(uuid4()))
    business_id = db.Column(db.String(100), db.ForeignKey('business.id', ondelete='cascade'), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    personnel_group_id = db.Column(db.String(100), db.ForeignKey('personnel_group.id', ondelete='cascade'),
                                   nullable=False)
    # amount = db.Column(db.Numeric(10, 2, asdecimal=False))
    disabled = db.Column(db.Boolean, default=False)
    notes = db.Column(db.Text, nullable=False)
    per_day = db.Column(db.Boolean, default=False)
    allowance = db.Column(db.Boolean, default=False)
    user_earnings = db.relationship('UserEarning', backref=db.backref('earning_group'),
                                    cascade='all,delete,delete-orphan',
                                    lazy='dynamic')


class Tax(db.Model, Record):
    id = db.Column(db.String(100), primary_key=True, nullable=False, unique=True, default=lambda: str(uuid4()))
    business_id = db.Column(db.String(100), db.ForeignKey('business.id', ondelete='cascade'), nullable=False)
    period_id = db.Column(db.String(100), db.ForeignKey('period.id', ondelete='cascade'), nullable=False)
    personnel_group_id = db.Column(db.String(100), db.ForeignKey('personnel_group.id', ondelete='cascade'),
                                   nullable=False)
    name = db.Column(db.String(50), nullable=False)
    rate = db.Column(db.Float, nullable=True)
    disabled = db.Column(db.Boolean, default=False)
    automate = db.Column(db.Boolean, default=True)
    notes = db.Column(db.Text, nullable=False)


class Attendance(db.Model, Record):
    id = db.Column(db.String(100), primary_key=True, nullable=False, unique=True, default=lambda: str(uuid4()))
    business_id = db.Column(db.String(100), db.ForeignKey('business.id', ondelete='cascade'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    day = db.Column(db.Date, nullable=False)
    period_id = db.Column(db.String(100), db.ForeignKey('period.id', ondelete='cascade'), nullable=False)
    disabled = db.Column(db.Boolean, default=False)
    notes = db.Column(db.Text, nullable=False)
    user_attendances = db.relationship('UserAttendance', backref=db.backref('attendance'),
                                       cascade='all,delete,delete-orphan',
                                       lazy='dynamic')
    # we track the attendance day and relate it to the
    # current day and allow yours to enter their attendance when they login


class UserAttendance(db.Model, Record):
    id = db.Column(db.String(100), primary_key=True, nullable=False, unique=True, default=lambda: str(uuid4()))
    business_id = db.Column(db.String(100), db.ForeignKey('business.id', ondelete='cascade'), nullable=False)
    user_meta_id = db.Column(db.String(100), db.ForeignKey('user_meta.id', ondelete='cascade'), nullable=False)
    attendance_id = db.Column(db.String(100), db.ForeignKey('attendance.id', ondelete='cascade'), nullable=False)
    attype = db.Column(db.Enum('Absent', 'Excused Duty', 'Present'), nullable=False)
    time = db.Column(db.String(50), nullable=False)
    type = db.Column(db.Enum('Clock In', 'Clock Out'), nullable=False)


class UserDeduction(db.Model, Record):
    id = db.Column(db.String(100), primary_key=True, nullable=False, unique=True, default=lambda: str(uuid4()))
    business_id = db.Column(db.String(100), db.ForeignKey('business.id', ondelete='cascade'), nullable=False)
    user_meta_id = db.Column(db.String(100), db.ForeignKey('user_meta.id', ondelete='cascade'), nullable=False)
    deduction_group_id = db.Column(db.String(100), db.ForeignKey('deduction_group.id', ondelete='cascade'),
                                   nullable=False)
    period_id = db.Column(db.String(100), db.ForeignKey('period.id', ondelete='cascade'), nullable=True)
    rate = db.Column(db.Float, nullable=True)
    disabled = db.Column(db.Boolean, default=False)
    # a user should be deducted buy the sme deduction group [Not duplication for same user_meta and deduction group]


class UserEarning(db.Model, Record):
    id = db.Column(db.String(100), primary_key=True, nullable=False, unique=True, default=lambda: str(uuid4()))
    business_id = db.Column(db.String(100), db.ForeignKey('business.id', ondelete='cascade'), nullable=False)
    user_meta_id = db.Column(db.String(100), db.ForeignKey('user_meta.id', ondelete='cascade'), nullable=False)
    earning_group_id = db.Column(db.String(100), db.ForeignKey('earning_group.id', ondelete='cascade'), nullable=False)
    period_id = db.Column(db.String(100), db.ForeignKey('period.id', ondelete='cascade'), nullable=True)
    rate = db.Column(db.Float, nullable=True)
    disabled = db.Column(db.Boolean, default=False)
    # a user should be deducted buy the sme earnings group [Not duplication for same user_meta and earning group]


class Queue(db.Model, Record):
    id = db.Column(db.String(100), primary_key=True, nullable=False, unique=True, default=lambda: str(uuid4()))
    business_id = db.Column(db.String(100), db.ForeignKey('business.id', ondelete='cascade'), nullable=False)
    job_name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)


class Setting(db.Model, Record):
    id = db.Column(db.String(100), primary_key=True, nullable=False, unique=True, default=lambda: str(uuid4()))
    business_id = db.Column(db.String(100), db.ForeignKey('business.id', ondelete='cascade'), nullable=False,
                            unique=True)
    retirement_age = db.Column(db.Integer, nullable=False, default=60)
    notify_payment_by_sms = db.Column(db.Boolean, default=False)
    notify_payment_by_email = db.Column(db.Boolean, default=False)
    enable_user_account = db.Column(db.Boolean, default=False)
    send_payslip = db.Column(db.Boolean, default=False)
    enable_user_portal = db.Column(db.Boolean, default=False)
    allow_tax_paye = db.Column(db.Boolean, default=True)
