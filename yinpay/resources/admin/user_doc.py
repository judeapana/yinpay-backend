from flask_jwt_extended import jwt_required, current_user
from flask_restplus import Resource, Namespace

from yinpay import flask_filter, pagination, db
from yinpay.common.localns import selector
from yinpay.models import UserDoc
from yinpay.schema import UserDocSchema

namespace = Namespace('user_doc', path='/user-doc', decorators=[jwt_required()])
schema = UserDocSchema()


class UserDocListResource(Resource):
    @namespace.expect(selector)
    def get(self):
        sel = selector.parse_args()
        search = current_user.business.filter_by(id=sel.selector).first_or_404().user_docs
        if namespace.payload:
            search = flask_filter.search(current_user.business.filter_by(id=sel.selector).first_or_404().user_docs,
                                         [namespace.payload.get('filters')], UserDocSchema(many=True),
                                         order_by=namespace.payload.get('order_by', 'created'))
        return pagination.paginate(search, schema, marshmallow=True)

    @namespace.expect(selector)
    def post(self):
        sel = selector.parse_args()
        bs = current_user.business.filter_by(id=sel.selector).first_or_404()
        user_doc = UserDoc()
        namespace.payload['business_id'] = bs.id
        user_doc = schema.load(namespace.payload, session=db.session, instance=user_doc, unknown='exclude')
        user_doc.save()
        return schema.dump(user_doc), 200


class UserDocResource(Resource):
    @namespace.expect(selector)
    def get(self, pk):
        sel = selector.parse_args()
        bs = current_user.business.filter_by(id=sel.selector).first_or_404()
        user_doc = UserDoc.query.filter(UserDoc.business_id == bs.id, UserDoc.id == pk).first_or_404()
        return schema.dump(user_doc), 200

    @namespace.expect(selector)
    def put(self, pk):
        sel = selector.parse_args()
        bs = current_user.business.filter_by(id=sel.selector).first_or_404()
        user_doc = UserDoc.query.filter(UserDoc.business_id == bs.id, UserDoc.id == pk).first_or_404()
        namespace.payload['business_id'] = bs.id
        user_doc = schema.load(namespace.payload, session=db.session, instance=user_doc, unknown='exclude')
        user_doc.save()
        return schema.dump(user_doc), 200

    @namespace.expect(selector)
    def delete(self, pk):
        sel = selector.parse_args()
        bs = current_user.business.filter_by(id=sel.selector).first_or_404()
        user_doc = UserDoc.query.filter(UserDoc.business_id == bs.id, UserDoc.id == pk).first_or_404()
        return user_doc.delete(), 200


namespace.add_resource(UserDocListResource, '/')
namespace.add_resource(UserDocResource, '/<pk>')
