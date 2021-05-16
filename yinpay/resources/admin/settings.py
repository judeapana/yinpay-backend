from flask_restplus import Resource, Namespace

namespace = Namespace('setting', path='/settings')


class SettingResource(Resource):
    def post(self):
        pass

    def put(self):
        pass


namespace.add_resource(SettingResource, '/setting')
