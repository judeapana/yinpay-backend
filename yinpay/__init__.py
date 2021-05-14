from flask import Flask

from yinpay.config import Development
from yinpay.ext import cors, maintenance, bcrypt, mail, migrate, redis, rq, paginate, ma, flask_filter
from yinpay.models import db


def create_app():
    app = Flask(__name__)
    app.config.from_object(Development)
    db.init_app(app)
    cors.init_app(app)
    mail.init_app(app)
    maintenance.init_app(app)
    bcrypt.init_app(app)
    migrate.init_app(app, db)
    redis.init_app(app)
    rq.init_app(app)
    paginate.init_app(app)
    ma.init_app(app)
    flask_filter.init_app(app)
    app.register_blueprint(v0)
    return app


from yinpay.api import v0
