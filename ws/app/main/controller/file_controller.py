from flask_restplus import Resource, Namespace, reqparse
from werkzeug.datastructures import FileStorage

from ..service import file_service

api = Namespace('file', description='file related operations')


@api.route('/upload')
class FileUpload(Resource):

    @api.doc('file_upload')
    def post(self):
        parse = reqparse.RequestParser()
        parse.add_argument('file', type=FileStorage, location=['files', 'form'])
        args = parse.parse_args()
        file = args['file']
        if file:
            file_service.save_file(file)
            return '', 200
        else:
            return 'No files found in request!', 400


@api.route('/<filename>')
@api.param('filename', 'The file name')
@api.response(404, 'File not found.')
class FileDownload(Resource):
    def get(self, filename):
        return file_service.get_file(filename)
