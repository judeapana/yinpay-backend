from datetime import timedelta


class Instance:
    APP_NAME = 'Yin-Pay'
    DEBUG = True
    ENV = 'development'
    MAIL_SERVER = '------'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    SECRET_KEY = 'c60c9f3a7422972d15030e4ffcdd89a59e6e4ffd'
    MAIL_USERNAME = '-----'
    MAIL_PASSWORD = "---"
    MAIL_DEFAULT_SENDER = '----'
    RQ_QUEUES = ['yin_pay_default']
    SQLALCHEMY_DATABASE_URI = '-----'
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
    SQLALCHEMY_DATABASE_URI = '----'
    # SQLALCHEMY_DATABASE_URI = '-----'
    SQLALCHEMY_POOL_RECYCLE = 299
    SQLALCHEMY_POOL_TIMEOUT = 20
    REDIS_URL = '-----'
    RQ_REDIS_URL = '---'
    MAIL_SERVER = '-----'
    MAIL_PORT = 587
    MAIL_USE_SSL = True
    MAIL_USERNAME = 'androapana'
    MAIL_PASSWORD = '-----'
    MAIL_DEFAULT_SENDER = '------'
