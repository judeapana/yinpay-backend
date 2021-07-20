from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_filter import FlaskFilter
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from flask_maintenance import Maintenance
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_redis import FlaskRedis
from flask_rest_paginate import Pagination
from flask_rq2 import RQ
from flask_sqlalchemy import SQLAlchemy

jwt = JWTManager()
cors = CORS()
maintenance = Maintenance()
db = SQLAlchemy()
bcrypt = Bcrypt()
mail = Mail()
migrate = Migrate()
redis = FlaskRedis(health_check_interval=30)
rq = RQ()
pagination = Pagination()
ma = Marshmallow()
flask_filter = FlaskFilter()
