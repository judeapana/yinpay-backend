import werkzeug
from flask import request
from flask_jwt_extended import jwt_required
from flask_restplus import Resource, Namespace
from flask_restplus.reqparse import RequestParser

from yinpay import User
from yinpay.common.helpers import img_upload, delete_file, file_upload
from yinpay.models import Business, UserDoc
from yinpay.schema import UserSchema, BusinessSchema, UserDocSchema

namespace = Namespace('upload_manager', description='', path='/upload', decorators=[jwt_required()])

parser = RequestParser(trim=True, bundle_errors=True)
parser.add_argument('img', type=werkzeug.datastructures.FileStorage, location='form')
parser.add_argument('loc', type=str, choices=['user', 'logo', 'doc'], location="query_string")

user_schema = UserSchema()
business_schema = BusinessSchema()
user_doc_schema = UserDocSchema()


class ImgUploadResource(Resource):
    def post(self, pk):
        file = request.files['img']
        filename = img_upload(file)
        if request.args.get('loc') == 'user':
            user = User.query.get.get_or_404(pk)
            user.img = filename
            user.save()
            return user_schema.dump(user)
        if request.args.get('loc') == 'logo':
            business = Business.query.get_or_404(pk)
            business.logo = filename
            business.save()
            return business_schema.dump(business)

    def put(self, pk):
        parser.add_argument('filename', type=str)
        res = parser.parse_args()
        filename = img_upload(res.file)
        if res.loc == 'user':
            user = User.query.get.get_or_404(pk)
            delete_file(user.img, base_dir='protected/img')
            user.img = filename
            user.save()
            return user_schema.dump(user)
        if res.loc == 'logo':
            business = Business.query.get_or_404(pk)
            delete_file(business.img, base_dir='protected/img')
            business.logo = filename
            business.save()
            return business_schema.dump(business)

    def delete(self, pk):
        parser.add_argument('filename', type=str)
        res = parser.parse_args()
        if res.loc == 'user':
            user = User.query.get.get_or_404(pk)
            delete_file(user.img, base_dir='protected/img')
            user.img = ''
            user.save()
            return user_schema.dump(user)
        if res.loc == 'logo':
            business = Business.query.get_or_404(pk)
            delete_file(business.img, base_dir='protected/img')
            business.logo = ''
            business.save()
            return business_schema.dump(business)


class FileUploadResource(Resource):
    def post(self, pk):
        res = parser.parse_args()
        filename = file_upload(res.file)
        if res.loc == 'doc':
            user_doc = UserDoc.query.get.get_or_404(pk)
            user_doc.doc = filename
            user_doc.save()
            return user_schema.dump(user_doc)

    def put(self, pk):
        res = parser.parse_args()
        filename = file_upload(res.file)

        if res.loc == 'doc':
            user_doc = UserDoc.query.get.get_or_404(pk)
            delete_file(user_doc.doc, base_dir='protected/file')
            user_doc.doc = filename
            user_doc.save()
            return user_doc_schema.dump(user_doc)

    def delete(self, pk):
        res = parser.parse_args()

        if res.loc == 'doc':
            user_doc = UserDoc.query.get.get_or_404(pk)
            delete_file(user_doc.doc, base_dir='protected/file')
            user_doc.doc = ''
            user_doc.save()

            return user_doc_schema.dump(user_doc)


namespace.add_resource(ImgUploadResource, '/img/<pk>')
namespace.add_resource(FileUploadResource, '/file/<pk>')
