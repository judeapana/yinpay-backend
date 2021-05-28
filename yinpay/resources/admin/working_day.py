from flask_jwt_extended import jwt_required, current_user
from flask_restplus import Resource, Namespace

from yinpay import flask_filter, pagination, db
from yinpay.common.localns import selector
from yinpay.models import WorkingDay
from yinpay.schema import WorkingDaySchema

namespace = Namespace('working_days', path='/working-day', decorators=[jwt_required()])

schema = WorkingDaySchema()


class WorkingDayResource(Resource):
    @namespace.expect(selector)
    def get(self):
        sel = selector.parse_args()
        search = current_user.business.filter_by(id=sel.selector).first_or_404().working_days
        if namespace.payload:
            search = flask_filter.search(current_user.business.filter_by(id=sel.selector).first_or_404().working_days,
                                         [namespace.payload.get('filters')], WorkingDaySchema(many=True),
                                         order_by=namespace.payload.get('order_by', 'created'))
        return pagination.paginate(search, schema, marshmallow=True)

    @namespace.expect(selector)
    def post(self):
        sel = selector.parse_args()
        bs = current_user.business.filter_by(id=sel.selector).first_or_404()
        wd = WorkingDay()
        namespace.payload['business_id'] = bs.id
        wd = schema.load(namespace.payload, session=db.session, instance=wd, unknown='exclude')
        wd.save()
        return schema.dump(wd), 200


class WorkingDayResourceList(Resource):
    @namespace.expect(selector)
    def get(self, pk):
        sel = selector.parse_args()
        bs = current_user.business.filter_by(id=sel.selector).first_or_404()
        wd = WorkingDay.query.filter(WorkingDay.business_id == bs.id, WorkingDay.id == pk).first_or_404()
        return schema.dump(wd), 200

    @namespace.expect(selector)
    def put(self, pk):
        sel = selector.parse_args()
        bs = current_user.business.filter_by(id=sel.selector).first_or_404()
        wd = WorkingDay.query.filter(WorkingDay.business_id == bs.id, WorkingDay.id == pk).first_or_404()
        namespace.payload['business_id'] = bs.id
        wd = schema.load(namespace.payload, session=db.session, instance=wd, unknown='exclude')
        wd.save()
        return schema.dump(wd), 200

    @namespace.expect(selector)
    def delete(self, pk):
        sel = selector.parse_args()
        bs = current_user.business.filter_by(id=sel.selector).first_or_404()
        wd = WorkingDay.query.filter(WorkingDay.business_id == bs.id, WorkingDay.id == pk).first_or_404()
        return wd.delete(), 200


namespace.add_resource(WorkingDayResource, '/')
namespace.add_resource(WorkingDayResourceList, '/<pk>')
