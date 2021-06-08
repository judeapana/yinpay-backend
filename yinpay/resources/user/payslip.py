from flask_restful.reqparse import RequestParser
from flask_restplus import Resource, Namespace

namespace = Namespace('Payslip', path='/user/payslip')

parser = RequestParser(bundle_errors=True, trim=True)
parser.add_argument('period', type=str, location='query_string')


class PayslipResourceList(Resource):
    def get(self):
        res = parser.parse_args()
        pass


class PayslipResource(Resource):
    def get(self, pk):
        pass
