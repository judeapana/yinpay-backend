from flask_jwt_extended import jwt_required, current_user
from flask_restplus import Resource, Namespace

from yinpay.common.localns import selector
from yinpay.ext import flask_filter, pagination, db
from yinpay.models import NextOfKin
from yinpay.schema import NextOfKinSchema

namespace = Namespace('nextOfKin', path='/next-of-kin', decorators=[jwt_required()])
schema = NextOfKinSchema()


class NextOfKinListResource(Resource):
    @namespace.expect(selector)
    def get(self):
        res = selector.parse_args()
        search = current_user.business.filter_by(id=res.selector).first_or_404().next_of_kins
        if namespace.payload:
            search = flask_filter.search(current_user.business.filter_by(id=res.selector).first_or_404().next_of_kins,
                                         [namespace.payload.get('filters')], NextOfKinSchema(many=True),
                                         order_by=namespace.payload.get('order_by', 'created'))
        return pagination.paginate(search, schema, marshmallow=True)

    @namespace.expect(selector)
    def post(self):
        res = selector.parse_args()
        bs = current_user.business.filter_by(id=res.selector).first_or_404()
        nok = NextOfKin()
        namespace.payload['business_id'] = bs.id
        nok = schema.load(namespace.payload, session=db.session, instance=nok, unknown='exclude')
        nok.save()
        return schema.dump(nok), 200


class NextOfKinResource(Resource):
    @namespace.expect(selector)
    def get(self, pk):
        res = selector.parse_args()
        bs = current_user.business.filter_by(id=res.selector).first_or_404()
        nok = NextOfKin.query.filter(NextOfKin.id == pk, NextOfKin.business_id == bs.id).first_or_404()
        return schema.dump(nok), 200

    @namespace.expect(selector)
    def put(self, pk):
        res = selector.parse_args()
        bs = current_user.business.filter_by(id=res.selector).first_or_404()
        nok = NextOfKin.query.filter(NextOfKin.id == pk, NextOfKin.business_id == bs.id).first_or_404()
        namespace.payload['business_id'] = bs.id
        nok = schema.load(namespace.payload, session=db.session, instance=nok, unknown='exclude')
        nok.save()
        return schema.dump(nok), 200

    @namespace.expect(selector)
    def delete(self, pk):
        res = selector.parse_args()
        bs = current_user.business.filter_by(id=res.selector).first_or_404()
        nok = NextOfKin.query.filter(NextOfKin.id == pk, NextOfKin.business_id == bs.id).first_or_404()
        return nok.delete(), 200


namespace.add_resource(NextOfKinListResource, '/')
namespace.add_resource(NextOfKinResource, '/<pk>')
