from flask_jwt_extended import jwt_required
from flask_restplus import Resource, Namespace

from yinpay.ext import flask_filter, pagination, db
from yinpay.models import Queue
from yinpay.schema import QueueSchema

namespace = Namespace('queue', path='/queue',decorators=[jwt_required()])
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
        queue = Queue.query.get_or_404(pk)
        return queue, 200

    def put(self, pk):
        queue = Queue.query.get_or_404(pk)
        queue = schema.load(namespace.payload, session=db.session, instance=queue, unknown='exclude')
        queue.save()
        return schema.dump(queue), 200

    def delete(self, pk):
        queue = Queue.query.get_or_404(pk)
        return queue.delete(), 200


namespace.add_resource(QueueListResource, '/')
namespace.add_resource(QueueResource, '/<pk>')
