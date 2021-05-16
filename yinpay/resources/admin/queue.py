from flask_restplus import Resource, Namespace

from yinpay import flask_filter, pagination
from yinpay.models import Queue
from yinpay.schema import QueueSchema

namespace = Namespace('queue', path='/queue')
schema = QueueSchema()


class QueueListResource(Resource):
    def get(self):
        search = Queue
        if namespace.payload:
            search = flask_filter.search(Queue, [namespace.payload.get('filters')], QueueSchema(many=True),
                                         order_by=namespace.payload.get('order_by', 'created'))
        return pagination.paginate(search, schema, marshmallow=True)


class QueueResource(Resource):
    def get(self, pk):
        pass

    def put(self, pk):
        pass

    def delete(self, pk):
        pass


namespace.add_resource(QueueListResource, '/')
namespace.add_resource(QueueResource, '/<pk>')
