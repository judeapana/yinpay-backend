from flask_restplus import Resource, Namespace

from yinpay import flask_filter, pagination, db
from yinpay.models import PersonnelGroup
from yinpay.schema import PersonnelGroupSchema

namespace = Namespace('PersoneelGroup', path='/personnel-group')

schema = PersonnelGroupSchema()


class PersonnelGroupListResource(Resource):
    def get(self):
        search = PersonnelGroup
        if namespace.payload:
            search = flask_filter.search(PersonnelGroup, [namespace.payload.get('filters')],
                                         PersonnelGroupSchema(many=True),
                                         order_by=namespace.payload.get('order_by', 'created'))
        return pagination.paginate(search, schema, marshmallow=True)

    def post(self):
        pg = PersonnelGroup()
        pg = schema.load(namespace.payload, session=db.session, instance=pg, unknown='exclude')
        pg.save()
        return schema.dump(pg), 200


class PersonnelGroupResource(Resource):
    def get(self, pk):
        pass

    def put(self, pk):
        pass

    def delete(self, pk):
        pass


namespace.add_resource(PersonnelGroupListResource, '/')
namespace.add_resource(PersonnelGroupResource, '/<pk>')
