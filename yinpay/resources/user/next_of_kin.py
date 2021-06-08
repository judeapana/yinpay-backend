from flask_jwt_extended import current_user
from flask_restplus import Resource, Namespace

from yinpay.ext import flask_filter, pagination, db
from yinpay.models import NextOfKin
from yinpay.schema import CurUserNextKinSchema

namespace = Namespace('userLeave', path='/user/next-of-kin')
schema = CurUserNextKinSchema()


class UserNextOfKinResourceList(Resource):
    def get(self):
        search = current_user.user_meta.next_of_kins
        if namespace.payload:
            search = flask_filter.search(current_user.user_meta.next_of_kins,
                                         [namespace.payload.get('filters')], CurUserNextKinSchema(many=True),
                                         order_by=namespace.payload.get('order_by', 'created'))
        return pagination.paginate(search, schema, marshmallow=True)

    def post(self):
        next_of_kin = NextOfKin()
        next_of_kin = schema.load(namespace.payload, session=db.session, instance=next_of_kin, unknown='exclude')
        next_of_kin.save()
        return schema.dump(next_of_kin), 200


class UserNextOfKinResource(Resource):
    def get(self, pk):
        next_of_kin = current_user.user_meta.next_of_kins.filter(NextOfKin.id == pk).first_or_404()
        return schema.dump(next_of_kin), 200

    def put(self, pk):
        next_of_kin = current_user.user_meta.next_of_kins.filter(NextOfKin.id == pk).first_or_404()
        next_of_kin = schema.load(namespace.payload, session=db.session, instance=next_of_kin, unknown='exclude')
        next_of_kin.save()
        return schema.dump(next_of_kin), 200

    def delete(self, pk):
        next_of_kin = current_user.user_meta.next_of_kins.filter(NextOfKin.id == pk).first_or_404()
        return next_of_kin.delete(), 200
