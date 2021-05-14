from flask_restplus import Resource

from yinpay.resources.security import namespace


@namespace.route('/')
class Login(Resource):
    def post(self):
        pass


@namespace.route('/refresh')
class Refresh(Resource):
    def post(self):
        pass


@namespace.route('/logout')
class Logout(Resource):
    def post(self):
        pass
