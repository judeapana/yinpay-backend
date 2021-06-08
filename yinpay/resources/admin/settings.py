from flask_jwt_extended import jwt_required, current_user
from flask_restplus import Resource, Namespace

from yinpay.common.localns import selector
from yinpay.ext import db
from yinpay.models import Setting
from yinpay.schema import SettingSchema

namespace = Namespace('setting', path='/setting', decorators=[jwt_required()])
schema = SettingSchema()


class SettingResource(Resource):
    @namespace.expect(selector)
    def get(self):
        sel = selector.parse_args()
        bs = current_user.business.filter_by(id=sel.selector).first_or_404()
        if not Setting.query.filter(Setting.business_id == bs.id).first():
            setting = Setting(business_id=bs.id)
            setting.save()
        return schema.dump(bs.setting), 200

    @namespace.expect(selector)
    def put(self):
        sel = selector.parse_args()
        bs = current_user.business.filter_by(id=sel.selector).first_or_404()
        namespace.payload['business_id'] = bs.id
        setting = schema.load(namespace.payload, session=db.session, instance=bs.setting, unknown='exclude')
        setting.save()
        return schema.dump(setting), 200


namespace.add_resource(SettingResource, '/')
