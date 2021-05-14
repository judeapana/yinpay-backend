from uuid import uuid4

from yinpay.ext import db


class User(db.Model):
    id = db.Column(db.String(100), primary_key=True, nullable=False, unique=True, default=lambda: str(uuid4()))
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(50), nullable=True)
    last_name = db.Column(db.String(50), nullable=True)
    email_address = db.Column(db.String(50), nullable=False, unique=True)
    phone_number = db.Column(db.String(100), nullable=True)
    img = db.Column(db.String(50), nullable=True)
    disabled = db.Column(db.Boolean, default=False)
    superuser = db.Column(db.Boolean, default=False)
    last_logged_in = db.Column(db.DateTime)
    notes = db.Column(db.Text)
    business = db.relationship('Business', backref=db.backref('user'), cascade='all,delete,delete-orphan',
                               lazy='dynamic')
    user_meta = db.relationship('UserMeta', backref=db.backref('user'), cascade='all,delete',
                                lazy=True, uselist=False)


class Business(db.Model):
    id = db.Column(db.String(100), primary_key=True, nullable=False, unique=True, default=lambda: str(uuid4()))
    user_id = db.Column(db.String(100), db.ForeignKey('user.id', ondelete='cascade'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.Text, nullable=False)
    support_email = db.Column(db.String(50), nullable=False)
    phone_number = db.Column(db.String(50), nullable=False)
    logo = db.Column(db.String(100), nullable=False)
    btype = db.Column(db.Enum('Nonprofit Organization', 'Sole Proprietorship', 'Partnership', 'Corporation',
                              'Limited Liability Company,'),
                      nullable=False)
    description = db.Column(db.Text, nullable=False)
    proof = db.Column(db.String(100))
    approved = db.Column(db.Boolean, default=False)
    accounts = db.relationship('BusinessAccount', backref=db.backref('business'), cascade='all,delete,delete-orphan',
                               lazy='dynamic')
    setting = db.relationship('Setting', backref=db.backref('business'), cascade='all,delete', lazy=True, uselist=False)


class BusinessAccount(db.Model):
    id = db.Column(db.String(100), primary_key=True, nullable=False, unique=True, default=lambda: str(uuid4()))
    business_id = db.Column(db.String(100), db.ForeignKey('business.id', ondelete='cascade'), nullable=False)
    account_type = db.Column(db.Enum('Bank Account', 'Mobile Money'))
    name = db.Column(db.String(50), nullable=False)
    account_number = db.Column(db.String(50), nullable=False)
    code = db.Column(db.String(50), nullable=False)
    account_name = db.Column(db.String(50), nullable=False)
    currency = db.Column(db.String(50), nullable=False)
    primary = db.Column(db.Boolean, default=True)
    # bank name


class PersonnelGroup(db.Model):
    id = db.Column(db.String(100), primary_key=True, nullable=False, unique=True, default=lambda: str(uuid4()))
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


class UserMeta(db.Model):
    id = db.Column(db.String(100), primary_key=True, nullable=False, unique=True, default=lambda: str(uuid4()))
    user_id = db.Column(db.String(100), db.ForeignKey('user.id', ondelete='cascade'), nullable=False)
    personnel_group_id = db.Column(db.String(100), db.ForeignKey('personnel_group.id', ondelete='cascade'),
                                   nullable=False)
    department_id = db.Column(db.String(100), db.ForeignKey('department.id', ondelete='cascade'), nullable=False)
    title = db.Column(db.Enum('MRS', 'MISS', 'MR', 'MS'), nullable=True)
    marital_status = db.Column(db.Enum('Married', 'Divorced', 'Widowed', 'Single'), nullable=False)
    gender = db.Column(db.Enum('Male', 'Female'), nullable=False)
    religion = db.Column(db.String(50), nullable=False)
    retired = db.Column(db.Boolean, default=False)
    resigned = db.Column(db.Boolean, default=False)
    dob = db.Column(db.Date)
    addr = db.Column(db.Text, nullable=True)
    ssn = db.Column(db.String(50), nullable=False)
    tin = db.Column(db.String(50), nullable=False)
    next_of_kins = db.relationship('NextOfKin', backref=db.backref('user_meta'), cascade='all,delete,delete-orphan',
                                   lazy='dynamic')
    bank_details = db.relationship('BankDetail', backref=db.backref('user_meta'), cascade='all,delete,delete-orphan',
                                   lazy='dynamic')
    leaves = db.relationship('UserLeave', backref=db.backref('user_meta'), cascade='all,delete,delete-orphan',
                             lazy='dynamic')
    docs = db.relationship('UserDoc', backref=db.backref('user_meta'), cascade='all,delete,delete-orphan',
                           lazy='dynamic')
    working_days = db.relationship('WorkingDays', backref=db.backref('user_meta'), cascade='all,delete,delete-orphan',
                                   lazy='dynamic')
    daily_rates = db.relationship('DailyRate', backref=db.backref('user_meta'), cascade='all,delete,delete-orphan',
                                  lazy='dynamic')
    attendances = db.relationship('UserAttendance', backref=db.backref('user_meta'), cascade='all,delete,delete-orphan',
                                  lazy='dynamic')


class NextOfKin(db.Model):
    id = db.Column(db.String(100), primary_key=True, nullable=False, unique=True, default=lambda: str(uuid4()))
    user_meta_id = db.Column(db.String(100), db.ForeignKey('user_meta.id', ondelete='cascade'), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    middle_name = db.Column(db.String(50), nullable=False)
    dob = db.Column(db.Date, nullable=False)
    img = db.Column(db.String(100), nullable=True)


class Bank(db.Model):
    id = db.Column(db.String(100), primary_key=True, nullable=False, unique=True, default=lambda: str(uuid4()))
    name = db.Column(db.String(50), nullable=False)
    notes = db.Column(db.Text, nullable=False)
    disabled = db.Column(db.Boolean, default=False)
    accounts = db.relationship('BankDetail', backref=db.backref('bank'), cascade='all,delete,delete-orphan',
                               lazy='dynamic')


class BankDetail(db.Model):
    id = db.Column(db.String(100), primary_key=True, nullable=False, unique=True, default=lambda: str(uuid4()))
    bank_id = db.Column(db.String(100), db.ForeignKey('bank.id', ondelete='cascade'), nullable=False)
    user_meta_id = db.Column(db.String(100), db.ForeignKey('user_meta.id', ondelete='cascade'), nullable=False)
    code = db.Column(db.String(50), nullable=True)
    no = db.Column(db.String(50), nullable=False)
    branch = db.Column(db.String(100), nullable=False)
    disabled = db.Column(db.Boolean, default=False)
    currency = db.Column(db.String(50), nullable=False)


class Memo(db.Model):
    id = db.Column(db.String(100), primary_key=True, nullable=False, unique=True, default=lambda: str(uuid4()))
    title = db.Column(db.String(50), nullable=False)
    date = db.Column(db.DateTime)
    text = db.Column(db.Text, nullable=False)


class UserLeave(db.Model):
    id = db.Column(db.String(100), primary_key=True, nullable=False, unique=True, default=lambda: str(uuid4()))
    user_meta_id = db.Column(db.String(100), db.ForeignKey('user_meta.id', ondelete='cascade'), nullable=False)
    without_pay = db.Column(db.Boolean, default=False)
    ltype = db.Column(db.String(50), nullable=False)
    from_date = db.Column(db.Date, nullable=False)
    to_date = db.Column(db.Date, nullable=False)
    reason = db.Column(db.Text, nullable=False)
    status = db.Column(db.Boolean, default=False)


class UserDoc(db.Model):
    id = db.Column(db.String(100), primary_key=True, nullable=False, unique=True, default=lambda: str(uuid4()))
    user_meta_id = db.Column(db.String(100), db.ForeignKey('user_meta.id', ondelete='cascade'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    notes = db.Column(db.Text, nullable=False)
    doc = db.Column(db.String(100), nullable=True)


class Department(db.Model):
    id = db.Column(db.String(100), primary_key=True, nullable=False, unique=True, default=lambda: str(uuid4()))
    name = db.Column(db.String(100), nullable=False)
    abbr = db.Column(db.String(100), nullable=True)
    disabled = db.Column(db.Boolean, default=False)
    notes = db.Column(db.Text, nullable=True)
    user = db.relationship('UserMeta', backref=db.backref('department'), cascade='all,delete,delete-orphan',
                           lazy='dynamic')


# //Payroll//////

class Period(db.Model):
    id = db.Column(db.String(100), primary_key=True, nullable=False, unique=True, default=lambda: str(uuid4()))
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


class WorkingDay(db.Model):
    id = db.Column(db.String(100), primary_key=True, nullable=False, unique=True, default=lambda: str(uuid4()))
    period_id = db.Column(db.String(100), db.ForeignKey('period.id', ondelete='cascade'), nullable=False)
    personnel_group_id = db.Column(db.String(100), db.ForeignKey('personnel_group.id', ondelete='cascade'),
                                   nullable=False)
    days = db.Column(db.Integer, nullable=False)
    hours = db.Column(db.Integer, nullable=False)
    disabled = db.Column(db.Boolean, default=False)
    notes = db.Column(db.Text, nullable=False)


class DailyRate(db.Model):
    id = db.Column(db.String(100), primary_key=True, nullable=False, unique=True, default=lambda: str(uuid4()))
    period_id = db.Column(db.String(100), db.ForeignKey('period.id', ondelete='cascade'), nullable=False)
    user_meta_id = db.Column(db.String(100), db.ForeignKey('user_meta.id', ondelete='cascade'), nullable=False)
    main_amount = db.Column(db.Numeric(10, 2, asdecimal=False), nullable=False)
    emergency_amount = db.Column(db.Numeric(10, 2, asdecimal=False), nullable=True)
    disabled = db.Column(db.Boolean, default=False)
    notes = db.Column(db.Text, nullable=False)


class SocialSecurityRate(db.Model):
    id = db.Column(db.String(100), primary_key=True, nullable=False, unique=True, default=lambda: str(uuid4()))
    period_id = db.Column(db.String(100), db.ForeignKey('period.id', ondelete='cascade'), nullable=False, unique=True)
    emp_rate = db.Column(db.Float, nullable=False)
    emper_rate = db.Column(db.Float, nullable=False)
    tier1 = db.Column(db.Float, nullable=False)
    tier2 = db.Column(db.Float, nullable=False)


class DeductionGroup(db.Model):
    id = db.Column(db.String(100), primary_key=True, nullable=False, unique=True, default=lambda: str(uuid4()))
    name = db.Column(db.String(50), nullable=False)
    personnel_group_id = db.Column(db.String(100), db.ForeignKey('personnel_group.id', ondelete='cascade'),
                                   nullable=False)
    amount = db.Column(db.Numeric(10, 2, asdecimal=False))
    disabled = db.Column(db.Boolean, default=False)
    notes = db.Column(db.Text, nullable=False)
    per_day = db.Column(db.Boolean, default=False)
    user_deductions = db.relationship('UserDeduction', backref=db.backref('DeductionGroup'),
                                      cascade='all,delete,delete-orphan',
                                      lazy='dynamic')


class EarningGroup(db.Model):
    id = db.Column(db.String(100), primary_key=True, nullable=False, unique=True, default=lambda: str(uuid4()))
    name = db.Column(db.String(50), nullable=False)
    personnel_group_id = db.Column(db.String(100), db.ForeignKey('personnel_group.id', ondelete='cascade'),
                                   nullable=False)
    amount = db.Column(db.Numeric(10, 2, asdecimal=False))
    disabled = db.Column(db.Boolean, default=False)
    notes = db.Column(db.Text, nullable=False)
    per_day = db.Column(db.Boolean, default=False)
    allowance = db.Column(db.Boolean, default=False)
    user_earnings = db.relationship('UserEarning', backref=db.backref('earning_group'),
                                    cascade='all,delete,delete-orphan',
                                    lazy='dynamic')


class Tax(db.Model):
    id = db.Column(db.String(100), primary_key=True, nullable=False, unique=True, default=lambda: uuid4())
    period_id = db.Column(db.String(100), db.ForeignKey('period.id', ondelete='cascade'), nullable=False, unique=True)
    personnel_group_id = db.Column(db.String(100), db.ForeignKey('personnel_group.id', ondelete='cascade'),
                                   nullable=False)
    name = db.Column(db.String(50), nullable=False)
    rate = db.Column(db.Float, nullable=True)
    disabled = db.Column(db.Boolean, default=False)
    automate = db.Column(db.Boolean, default=True)
    notes = db.Column(db.Text, nullable=False)


class Attendance(db.Model):
    id = db.Column(db.String(100), primary_key=True, nullable=False, unique=True, default=lambda: str(uuid4()))
    name = db.Column(db.String(100), nullable=False)
    period_id = db.Column(db.String(100), db.ForeignKey('period.id', ondelete='cascade'), nullable=False, unique=True)
    disabled = db.Column(db.Boolean, default=False)
    notes = db.Column(db.Text, nullable=False)
    user_attendances = db.relationship('UserAttendance', backref=db.backref('attendance'),
                                       cascade='all,delete,delete-orphan',
                                       lazy='dynamic')


class UserAttendance(db.Model):
    id = db.Column(db.String(100), primary_key=True, nullable=False, unique=True, default=lambda: str(uuid4()))
    user_meta_id = db.Column(db.String(100), db.ForeignKey('user_meta.id', ondelete='cascade'), nullable=False)
    attendance_id = db.Column(db.String(100), db.ForeignKey('attendance.id', ondelete='cascade'), nullable=False)
    attype = db.Column(db.Enum('Absent', 'Excused Duty', 'Present'), nullable=False)
    date = db.Column(db.Date, nullable=False)


class UserDeduction(db.Model):
    id = db.Column(db.String(100), primary_key=True, nullable=False, unique=True, default=lambda: str(uuid4()))
    user_meta_id = db.Column(db.String(100), db.ForeignKey('user_meta.id', ondelete='cascade'), nullable=False)
    deduction_group_id = db.Column(db.String(100), db.ForeignKey('deduction_group.id', ondelete='cascade'),
                                   nullable=False)
    rate = db.Column(db.Float, nullable=True)
    disabled = db.Column(db.Boolean, default=False)


class UserEarning(db.Model):
    id = db.Column(db.String(100), primary_key=True, nullable=False, unique=True, default=lambda: str(uuid4()))
    user_meta_id = db.Column(db.String(100), db.ForeignKey('user_meta.id', ondelete='cascade'), nullable=False)
    earning_group_id = db.Column(db.String(100), db.ForeignKey('earning_group.id', ondelete='cascade'), nullable=False)
    rate = db.Column(db.Float, nullable=True)
    disabled = db.Column(db.Boolean, default=False)


class Queue(db.Model):
    id = db.Column(db.String(100), primary_key=True, nullable=False, unique=True, default=lambda: str(uuid4()))
    job_name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)


class Setting(db.Model):
    id = db.Column(db.String(100), primary_key=True, nullable=False, unique=True, default=lambda: str(uuid4()))
    business_id = db.Column(db.String(100), db.ForeignKey('business.id', ondelete='cascade'), nullable=False,
                            unique=True)
    atm_tax = db.Column(db.Boolean, nullable=False)
    retirement_age = db.Column(db.Integer, nullable=False)
    notify_payment_by_sms = db.Column(db.Boolean, default=False)
    notify_payment_by_email = db.Column(db.Boolean, default=False)
    enable_user_account = db.Column(db.Boolean, default=False)
    enable_otp_verification = db.Column(db.Boolean, default=False)
    send_payslip = db.Column(db.Boolean, default=False)
    enable_user_portal = db.Column(db.Boolean, default=False)
