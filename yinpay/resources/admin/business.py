from flask_jwt_extended import jwt_required, current_user
from flask_restplus import Resource, Namespace, fields

from yinpay.ext import flask_filter, pagination, db
from yinpay.schema import BusinessSchema
from ...models import Business

namespace = Namespace('business', description='', path='/business', decorators=[jwt_required()])
schema = BusinessSchema()

model = namespace.model('Business', {
    'name': fields.String(),
    'address': fields.String(),
    'support_email': fields.String(),
    'phone_number': fields.String(),
    'btype': fields.String(),
    'description': fields.String(),
    # 'setting':fields.Nested()
})


class BusinessListResource(Resource):

    def get(self):
        search = Business
        if namespace.payload:
            search = flask_filter.search(current_user.business, [namespace.payload.get('filters')],
                                         BusinessSchema(many=True),
                                         order_by=namespace.payload.get('order_by', 'created'))
        return pagination.paginate(search, schema, marshmallow=True)

    @namespace.expect(model)
    def post(self):
        business = Business()
        business = schema.load(namespace.payload, session=db.session, instance=business, unknown='exclude')
        current_user.business.append(business)
        current_user.save()

        return schema.dump(business), 200


class BusinessResource(Resource):
    def get(self, pk):
        business = current_user.business.filter(Business.id == pk).first_or_404()
        return business, 200

    def put(self, pk):
        business = current_user.business.filter(Business.id == pk).first_or_404()
        business = schema.load(namespace.payload, session=db.session, instance=business, unknown='exclude')
        business.save()
        return schema.dump(business), 200

    def delete(self, pk):
        business = current_user.business.filter(Business.id == pk).first_or_404()
        return business.delete(), 200


namespace.add_resource(BusinessListResource, '/')
namespace.add_resource(BusinessResource, '/<pk>')
