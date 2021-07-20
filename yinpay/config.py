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
    # RQ_QUEUES = ['yin_pay_default']
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
    SQLALCHEMY_DATABASE_URI = 'postgresql://ysawxzjywtlhho:17d302684b872bc26b9e1b7d67d37c69d4e4b145728064344de7b5febec0a712@ec2-54-155-35-88.eu-west-1.compute.amazonaws.com:5432/d2loof4nu52h90'
    SQLALCHEMY_POOL_RECYCLE = 299
    SQLALCHEMY_POOL_TIMEOUT = 20
    RQ_REDIS_URL = 'redis://:pc49c90ac53ed968ebc4264255032c88d1454cf13adc9f67469120159f4703204@ec2-54-195-111-186.eu-west-1.compute.amazonaws.com:15750'
    MAIL_SERVER = 'smtp.mailtrap.io'
    MAIL_PORT = 2525
    MAIL_USERNAME = 'ccbfa2ade54399'
    MAIL_PASSWORD = '15ea0cf79e0bfb'
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
