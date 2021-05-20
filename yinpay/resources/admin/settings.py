from flask_jwt_extended import jwt_required
from flask_restplus import Resource, Namespace

from yinpay.ext import db
from yinpay.models import Setting
from yinpay.schema import SettingSchema

namespace = Namespace('setting', path='/setting',decorators=[jwt_required()])
schema = SettingSchema()


class SettingResource(Resource):
    def get(self):
        setting = Setting.query.get_or_404()
        return setting, 200

    def put(self, pk):
        setting = Setting.query.get_or_404(pk)
        setting = schema.load(namespace.payload, session=db.session, instance=setting, unknown='exclude')
        setting.save()
        return schema.dump(setting), 200


namespace.add_resource(SettingResource, '/setting')
