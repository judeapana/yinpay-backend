from flask import Blueprint
from flask_restplus import Api

yinapi = Blueprint('api', __name__, url_prefix='/')

api = Api(yinapi, title='YinPay API',)
