from flask_jwt_extended import jwt_required
from flask_restplus import Resource, Namespace

from yinpay import flask_filter, pagination, db
from yinpay.models import UserDoc
from yinpay.schema import UserDocSchema

namespace = Namespace('user_doc', path='/user-doc',decorators=[jwt_required()])
schema = UserDocSchema()


class UserDocListResource(Resource):
    def get(self):
        search = UserDoc
        if namespace.payload:
            search = flask_filter.search(UserDoc, [namespace.payload.get('filters')], UserDocSchema(many=True),
                                         order_by=namespace.payload.get('order_by', 'created'))
        return pagination.paginate(search, schema, marshmallow=True)

    def post(self):
        user_doc = UserDoc()
        user_doc = schema.load(namespace.payload, session=db.session, instance=user_doc, unknown='exclude')
        user_doc.save()
        return schema.dump(user_doc), 200


class UserDocResource(Resource):
    def get(self, pk):
        user_doc = UserDoc.query.get_or_404(pk)
        return user_doc, 200

    def put(self, pk):
        user_doc = UserDoc.query.get_or_404(pk)
        user_doc = schema.load(namespace.payload, session=db.session, instance=user_doc, unknown='exclude')
        user_doc.save()
        return schema.dump(user_doc), 200

    def delete(self, pk):
        user_doc = UserDoc.query.get_or_404(pk)
        return user_doc.delete(), 200


namespace.add_resource(UserDocListResource, '/')
namespace.add_resource(UserDocResource, '/<pk>')
