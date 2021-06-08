from flask_jwt_extended import current_user
from flask_restplus import Resource, Namespace

from yinpay.ext import flask_filter, pagination
from yinpay.models import UserDoc
from yinpay.schema import CurrentUserDocSchema

namespace = Namespace('userDocs', path='/user/docs')

schema = CurrentUserDocSchema()


class UserDocResourceList(Resource):
    def get(self):
        search = current_user.user_meta.user_earnings
        if namespace.payload:
            search = flask_filter.search(current_user.user_meta.user_deductions,
                                         [namespace.payload.get('filters')], CurrentUserDocSchema(many=True),
                                         order_by=namespace.payload.get('order_by', 'created'))
        return pagination.paginate(search, schema, marshmallow=True)


class UserDocResource(Resource):
    def get(self, pk):
        doc = current_user.user_meta.user_docs.filter(UserDoc.id == pk).first_or_404()
        return schema.dump(doc), 200
