# app/__init__.py

from flask_restplus import Api
from flask import Blueprint

from .main.controller.file_controller import api as file_ns

blueprint = Blueprint('api', __name__)

api = Api(blueprint,
          title='FILE UPLOAD API',
          version='1.0',
          description='file upload web service'
          )

api.add_namespace(file_ns, path='/file')