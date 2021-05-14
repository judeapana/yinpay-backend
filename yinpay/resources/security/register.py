from flask_restplus import Resource

from yinpay.resources.security import namespace


@namespace.route('/register')
class Register(Resource):
    def post(self):
        pass
