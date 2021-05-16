import werkzeug
from flask_restplus import Resource, Namespace
from flask_restplus.reqparse import RequestParser

namespace = Namespace('upload_manager', description='', path='/upload')

parser = RequestParser(trim=True, bundle_errors=True)
parser.add_argument('img', type=werkzeug.datastructures.FileStorage, location='files')
parser.add_argument('loc', type=str, choices=['user', 'logo'])


class ImgUploadResource(Resource):
    def post(self, pk):
        pass

    def put(self, pk):
        pass


class FileUploadResource(Resource):
    def post(self, pk):
        pass

    def put(self, pk):
        pass


namespace.add_resource(ImgUploadResource, '/img/<uuid>')
namespace.add_resource(FileUploadResource, '/file/<uuid>')
