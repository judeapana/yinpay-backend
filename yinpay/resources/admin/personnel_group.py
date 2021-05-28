from flask import request
from flask_jwt_extended import jwt_required, current_user
from flask_restplus import Resource, Namespace

from yinpay.common.localns import selector
from yinpay.ext import flask_filter, pagination, db
from yinpay.models import PersonnelGroup
from yinpay.schema import PersonnelGroupSchema

namespace = Namespace('PersonnelGroup', path='/personnel-group', decorators=[jwt_required()])

schema = PersonnelGroupSchema()
model = namespace.model('PersonnelGroup', {})


class PersonnelGroupListResource(Resource):
    @namespace.expect(selector)
    def get(self):
        args = selector.parse_args()
        search = current_user.business.filter_by(id=args.selector).first_or_404().personnel_groups
        if namespace.payload:
            search = flask_filter.search(
                current_user.business.filter_by(id=args.selector).first_or_404().personnel_groups,
                [namespace.payload.get('filters')],
                PersonnelGroupSchema(many=True),
                order_by=namespace.payload.get('order_by', 'created'))
        return pagination.paginate(search, schema, marshmallow=True)

    @namespace.param('selector')
    @namespace.expect(model)
    def post(self):
        pg = current_user.business.filter_by(id=request.args.get('selector')).first_or_404()
        namespace.payload['business_id'] = pg.id
        pg = schema.load(namespace.payload, session=db.session, unknown='exclude')
        pg.save()
        return schema.dump(pg), 200


class PersonnelGroupResource(Resource):
    @namespace.param('selector')
    def get(self, pk):
        pg = current_user.business.filter_by(id=request.args.get('selector')).first_or_404()
        pg = PersonnelGroup.query.filter_by(business_id=pg.id, id=pk).first_or_404()
        return schema.dump(pg), 200

    @namespace.param('selector')
    @namespace.expect(model)
    def put(self, pk):
        pg = current_user.business.filter_by(id=request.args.get('selector')).first_or_404()
        namespace.payload['business_id'] = pg.id
        pg = PersonnelGroup.query.get_or_404(pk)
        pg = schema.load(namespace.payload, session=db.session, instance=pg, unknown='exclude')
        pg.save()
        return schema.dump(pg), 200

    @namespace.param('selector')
    def delete(self, pk):
        pg = current_user.business.filter_by(id=request.args.get('selector')).first_or_404()
        pg = PersonnelGroup.query.filter_by(business_id=pg.id, id=pk).first_or_404()
        return pg.delete(), 200


namespace.add_resource(PersonnelGroupListResource, '/')
namespace.add_resource(PersonnelGroupResource, '/<pk>')
