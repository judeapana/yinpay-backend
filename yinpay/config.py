from datetime import timedelta


class Instance:
    APP_NAME = 'Yin-Pay'
    DEBUG = True
    ENV = 'development'
    MAIL_SERVER = 'mail.privateemail.com'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    SECRET_KEY = 'c60c9f3a7422972d15030e4ffcdd89a59e6e4ffd'
    MAIL_USERNAME = 'no-reply@yinime.com'
    MAIL_PASSWORD = "apana1jude1"
    MAIL_DEFAULT_SENDER = 'no-reply@yinime.com'
    RQ_QUEUES = ['yin_pay_default']
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root@localhost/yin_pay'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=40)
    # JWT_ACCESS_TOKEN_EXPIRES = timedelta(seconds=5)

    PAGINATE_PAGE_SIZE = 5
    # PAGINATE_RESOURCE_LINKS_ENABLED = False


class Development(Instance):
    pass


class Production(Instance):
    DEBUG = False
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=2)
    ENV = 'production'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:Apana1jude1$$@localhost/yin_pay'
    SQLALCHEMY_POOL_RECYCLE = 299
    SQLALCHEMY_POOL_TIMEOUT = 20
