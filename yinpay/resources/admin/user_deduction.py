from flask_restplus import Resource, Namespace

from yinpay import flask_filter, pagination, db
from yinpay.models import UserDeduction
from yinpay.schema import UserDeductionSchema

namespace = Namespace('user_deduction', path='/user-deduction')

schema = UserDeductionSchema()


class UserDeductionListResource(Resource):
    def get(self):
        search = UserDeduction
        if namespace.payload:
            search = flask_filter.search(UserDeduction, [namespace.payload.get('filters')],
                                         UserDeductionSchema(many=True),
                                         order_by=namespace.payload.get('order_by', 'created'))
        return pagination.paginate(search, schema, marshmallow=True)

    def post(self):
        ug = UserDeduction()
        ug = schema.load(namespace.payload, session=db.session, instance=ug, unknown='exclude')
        ug.save()
        return schema.dump(ug), 200


class UserDeductionResource(Resource):
    def get(self, pk):
        ug = UserDeduction.query.get_or_404(pk)
        return ug, 200

    def put(self, pk):
        ug = UserDeduction.query.get_or_404(pk)
        ug = schema.load(namespace.payload, session=db.session, instance=ug, unknown='exclude')
        ug.save()
        return schema.dump(ug), 200

    def delete(self, pk):
        ug = UserDeduction.query.get_or_404(pk)
        return ug.delete(), 200


namespace.add_resource(UserDeductionListResource, '/')
namespace.add_resource(UserDeductionResource, '/<pk>')
