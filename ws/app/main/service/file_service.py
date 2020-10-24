import os
import pathlib
import uuid
from datetime import datetime

from flask import send_from_directory, send_file
from werkzeug.utils import secure_filename

from ..dao import file_metadata_dao
from ..dao.model.file_metadata import FileMetadata
from . import aws_service
from . import subscriptionService

basedir = os.path.abspath(os.path.dirname(__file__))
DEFAULT_REGION = 'eu-west-1'


def save_file(file):
    filename = secure_filename(file.filename)
    ext = pathlib.Path(filename).suffix
    filename = pathlib.Path(filename).stem
    file_uuid = uuid.uuid4()
    dt = datetime.now()

    file_metadata = FileMetadata(filename, file_uuid, ext, dt)
    file_metadata_dao.save(file_metadata)

    __save_file_to_s3(file, str(file_uuid))
    subscriptionService.publish()
    # __save_file_locally(file, str(file_uuid))


def get_file(filename):
    filename = pathlib.Path(filename).stem
    file_metadata = file_metadata_dao.find_by_filename(filename)
    return __get_file_from_s3(file_metadata.uuid, ''.join([file_metadata.filename, file_metadata.extension]))
    # return __get_file_locally(file_metadata.uuid)


def get_random_file():
    file_metadata = file_metadata_dao.find_random()
    return __get_file_from_s3(file_metadata.uuid, ''.join([file_metadata.filename, file_metadata.extension]))



def __save_file_locally(file, filename):
    if not filename or filename == '':
        filename = uuid.uuid4()
    save_path = os.path.join(basedir, filename)
    file.save(save_path)


def __get_file_locally(file_uuid):
    return send_from_directory(basedir, file_uuid, as_attachment=True)


def __save_file_to_s3(file, filename):
    aws_service.save_file_to_s3(file, filename)


def __get_file_from_s3(file_uuid, filename):
    file = aws_service.get_file_from_s3(file_uuid)
    return send_file(file, attachment_filename=filename, as_attachment=True)
