from flask_restplus import Resource, Namespace

from yinpay.ext import flask_filter, pagination, db
from yinpay.models import NextOfKin
from yinpay.schema import NextOfKinSchema

namespace = Namespace('next_of_kin', path='/next-of-kin')
schema = NextOfKinSchema()


class NextOfKinListResource(Resource):
    def get(self):
        search = NextOfKin
        if namespace.payload:
            search = flask_filter.search(NextOfKin, [namespace.payload.get('filters')], NextOfKinSchema(many=True),
                                         order_by=namespace.payload.get('order_by', 'created'))
        return pagination.paginate(search, schema, marshmallow=True)

    def post(self):
        nok = NextOfKin()
        nok = schema.load(namespace.payload, session=db.session, instance=nok, unknown='exclude')
        nok.save()
        return schema.dump(nok), 200


class NextOfKinResource(Resource):
    def get(self, pk):
        nok = NextOfKin.query.get_or_404(pk)
        return nok, 200

    def put(self, pk):
        nok = NextOfKin.query.get_or_404(pk)
        nok = schema.load(namespace.payload, session=db.session, instance=nok, unknown='exclude')
        nok.save()
        return schema.dump(nok), 200

    def delete(self, pk):
        nok = NextOfKin.query.get_or_404(pk)
        return nok.delete(), 200


namespace.add_resource(NextOfKinListResource, '/')
namespace.add_resource(NextOfKinResource, '/<pk>')
