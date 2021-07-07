import os

from flask import send_from_directory, current_app
from flask_restplus import Namespace, fields, Resource

namespace = Namespace('ns', description='Local Namespace')

timestamp = namespace.model('TimestampMixin', {
    'id': fields.String(readonly=True),
    'updated': fields.DateTime(dt_format='rfc822', readonly=True),
    'created': fields.DateTime(dt_format='rfc822', readonly=True),
})

filters = namespace.model('FilterMixin', {
    'field': fields.String(),
    'op': fields.String(),
    'value': fields.String(),
})

search = namespace.model('SearchMixin', {
    'filters': fields.Nested(filters),
    'order_by': fields.String(default='created')
})

selector = namespace.parser()
selector.add_argument('selector', required=True, type=str, location='args')


class ProtectedDirResource(Resource):

    def get(self, filename):
        return send_from_directory(os.path.join(current_app.root_path, 'static', 'protected'),
                                   filename=filename)


namespace.add_resource(ProtectedDirResource, '/static/<filename>', endpoint='protected_dir')
