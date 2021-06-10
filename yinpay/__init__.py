from flask import Flask

from yinpay.config import Development
from yinpay.ext import cors, maintenance, bcrypt, mail, migrate, redis, rq, pagination, ma, flask_filter, jwt
from yinpay.models import db, User


def create_app():
    app = Flask(__name__)
    app.config.from_object(Development)
    db.init_app(app)
    cors.init_app(app, resources={r"/*": {"origins": "*"}})
    mail.init_app(app)
    maintenance.init_app(app)
    bcrypt.init_app(app)
    migrate.init_app(app, db)
    redis.init_app(app)
    rq.init_app(app)
    pagination.init_app(app, db)
    ma.init_app(app)
    flask_filter.init_app(app)
    app.register_blueprint(v0)
    jwt.init_app(app)

    @jwt.user_identity_loader
    def load_user(user):
        return user.id

    @jwt.user_lookup_loader
    def user_lookup(jwt_header, jwt_data):
        identity = jwt_data['sub']
        return User.query.filter_by(id=identity).one_or_none()

    @jwt.token_in_blocklist_loader
    def blacklist_token(jwt_header, jwt_data):
        jwt_token_identity = jwt_data['jti']
        token = redis.get(jwt_token_identity)
        return token is not None

    return app


from yinpay.api import v0
