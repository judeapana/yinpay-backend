from flask_restplus import Resource

from yinpay.resources.security import namespace


@namespace.route('/reset-pwd')
class ResetPwd(Resource):
    def get(self):
        pass

    def put(self):
        pass


@namespace.route('/forgot-pwd')
class ForgotPassword(Resource):
    def post(self):
        pass
