from flask_restplus import Resource, Namespace

from yinpay import flask_filter, pagination, db
from yinpay.models import UserEarning
from yinpay.schema import UserEarningSchema

namespace = Namespace('user_earning', path='/user-earning')

schema = UserEarningSchema()


class UserEarningListResource(Resource):
    def get(self):
        search = UserEarning
        if namespace.payload:
            search = flask_filter.search(UserEarning, [namespace.payload.get('filters')], UserEarningSchema(many=True),
                                         order_by=namespace.payload.get('order_by', 'created'))
        return pagination.paginate(search, schema, marshmallow=True)

    def post(self):
        user_earning = UserEarning()
        user_earning = schema.load(namespace.payload, session=db.session, instance=user_earning, unknown='exclude')
        user_earning.save()
        return schema.dump(user_earning), 200


class UserEarningResource(Resource):
    def get(self, pk):
        user_earning = UserEarning.query.get_or_404(pk)
        return user_earning, 200

    def put(self, pk):
        user_earning = UserEarning.query.get_or_404(pk)
        user_earning = schema.load(namespace.payload, session=db.session, instance=user_earning, unknown='exclude')
        user_earning.save()
        return schema.dump(user_earning), 200

    def delete(self, pk):
        user_earning = UserEarning.query.get_or_404(pk)
        return user_earning.delete(), 200


namespace.add_resource(UserEarningListResource, '/')
namespace.add_resource(UserEarningResource, '/<pk>')
