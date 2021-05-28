from flask_jwt_extended import jwt_required, current_user
from flask_restplus import Resource, Namespace

from yinpay.common.localns import selector
from yinpay.ext import flask_filter, pagination, db
from yinpay.models import Memo
from yinpay.schema import MemoSchema

namespace = Namespace('Memo', path='/memo', decorators=[jwt_required()])

schema = MemoSchema()


class MemoListResource(Resource):
    @namespace.expect(selector)
    def get(self):
        res = selector.parse_args()
        search = current_user.business.filter_by(id=res.selector).first_or_404().memos
        if namespace.payload:
            search = flask_filter.search(current_user.business.filter_by(id=res.selector).first_or_404().memos,
                                         [namespace.payload.get('filters')], MemoSchema(many=True),
                                         order_by=namespace.payload.get('order_by', 'created'))
        return pagination.paginate(search, schema, marshmallow=True)

    @namespace.expect(selector)
    def post(self):
        res = selector.parse_args()
        bs = current_user.business.filter_by(id=res.selector).first_or_404()
        memo = Memo()
        namespace.payload['business_id'] = bs.id
        memo = schema.load(namespace.payload, session=db.session, instance=memo, unknown='exclude')
        memo.save()
        return schema.dump(memo), 200


class MemoResource(Resource):
    @namespace.expect(selector)
    def get(self, pk):
        res = selector.parse_args()
        bs = current_user.business.filter_by(id=res.selector).first_or_404()
        memo = Memo.query.filter(Memo.id == pk, Memo.business_id == bs.id).first_or_404()
        return schema.dump(memo), 200

    @namespace.expect(selector)
    def put(self, pk):
        res = selector.parse_args()
        bs = current_user.business.filter_by(id=res.selector).first_or_404()
        memo = Memo.query.filter(Memo.id == pk, Memo.business_id == bs.id).first_or_404()
        namespace.payload['business_id'] = bs.id
        memo = schema.load(namespace.payload, session=db.session, instance=memo, unknown='exclude')
        memo.save()
        return schema.dump(memo), 200

    @namespace.expect(selector)
    def delete(self, pk):
        res = selector.parse_args()
        bs = current_user.business.filter_by(id=res.selector).first_or_404()
        memo = Memo.query.filter(Memo.id == pk, Memo.business_id == bs.id).first_or_404()
        return memo.delete(), 200


namespace.add_resource(MemoListResource, '/')
namespace.add_resource(MemoResource, '/<pk>')
