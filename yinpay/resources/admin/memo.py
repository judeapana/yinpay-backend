from flask_restplus import Resource, Namespace

from yinpay import flask_filter, pagination, db
from yinpay.models import Memo
from yinpay.schema import MemoSchema

namespace = Namespace('Memo', path='/memo')

schema = MemoSchema()


class MemoListResource(Resource):
    def get(self):
        search = Memo
        if namespace.payload:
            search = flask_filter.search(Memo, [namespace.payload.get('filters')], MemoSchema(many=True),
                                         order_by=namespace.payload.get('order_by', 'created'))
        return pagination.paginate(search, schema, marshmallow=True)

    def post(self):
        memo = Memo()
        memo = schema.load(namespace.payload, session=db.session, instance=memo, unknown='exclude')
        memo.save()
        return schema.dump(memo), 200


class MemoResource(Resource):
    def get(self, pk):
        pass

    def put(self, pk):
        pass

    def delete(self, pk):
        pass


namespace.add_resource(MemoListResource, '/')
namespace.add_resource(MemoResource, '/<pk>')
