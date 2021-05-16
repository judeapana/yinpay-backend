from flask_restplus import Resource, Namespace

from yinpay import flask_filter, pagination, db
from yinpay.models import SocialSecurityRate
from yinpay.schema import SocialSecurityRateSchema

namespace = Namespace('ssr', path='/ssr')

schema = SocialSecurityRateSchema()


class SocialSrListResource(Resource):
    def get(self):
        search = SocialSecurityRate
        if namespace.payload:
            search = flask_filter.search(SocialSecurityRate, [namespace.payload.get('filters')],
                                         SocialSecurityRateSchema(many=True),
                                         order_by=namespace.payload.get('order_by', 'created'))
        return pagination.paginate(search, schema, marshmallow=True)

    def post(self):
        ssr = SocialSecurityRate()
        ssr = schema.load(namespace.payload, session=db.session, instance=ssr, unknown='exclude')
        ssr.save()
        return schema.dump(ssr), 200


class SocialSrResource(Resource):
    def get(self, pk):
        pass

    def put(self, pk):
        pass

    def delete(self, pk):
        pass


namespace.add_resource(SocialSrListResource, '/')
namespace.add_resource(SocialSrResource, '/<pk>')
