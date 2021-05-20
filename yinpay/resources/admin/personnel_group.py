from flask_jwt_extended import jwt_required
from flask_restplus import Resource, Namespace

from yinpay.ext import flask_filter, pagination, db
from yinpay.models import PersonnelGroup
from yinpay.schema import PersonnelGroupSchema

namespace = Namespace('PersoneelGroup', path='/personnel-group',decorators=[jwt_required()])

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
        pg = PersonnelGroup.query.get_or_404(pk)
        return pg, 200

    def put(self, pk):
        pg = PersonnelGroup.query.get_or_404(pk)
        pg = schema.load(namespace.payload, session=db.session, instance=pg, unknown='exclude')
        pg.save()
        return schema.dump(pg), 200

    def delete(self, pk):
        pg = PersonnelGroup.query.get_or_404(pk)
        return pg.delete(), 200


namespace.add_resource(PersonnelGroupListResource, '/')
namespace.add_resource(PersonnelGroupResource, '/<pk>')
