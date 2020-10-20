import io
import os
import pathlib
import uuid
from datetime import datetime

import boto3
from flask import send_from_directory, send_file
from werkzeug.utils import secure_filename

from ..dao import file_metadata_dao
from ..dao.model.file_metadata import FileMetadata

basedir = os.path.abspath(os.path.dirname(__file__))
REGION = 'eu-west-1'


def save_file(file):
    filename = secure_filename(file.filename)
    ext = pathlib.Path(filename).suffix
    filename = pathlib.Path(filename).stem
    file_uuid = uuid.uuid4()
    dt = datetime.now()

    file_metadata = FileMetadata(filename, file_uuid, ext, dt)
    file_metadata_dao.save(file_metadata)

    __save_file_to_s3(file, str(file_uuid))
    # __save_file_locally(file, str(file_uuid))


def get_file(filename):
    filename = pathlib.Path(filename).stem
    file_metadata = file_metadata_dao.find_by_filename(filename)
    return __get_file_from_s3(file_metadata.uuid, ''.join([file_metadata.filename, file_metadata.extension]))
    # return __get_file_locally(file_metadata.uuid)


def __save_file_locally(file, filename):
    if not filename or filename == '':
        filename = uuid.uuid4()
    save_path = os.path.join(basedir, filename)
    file.save(save_path)


def __get_file_locally(file_uuid):
    return send_from_directory(basedir, file_uuid, as_attachment=True)


def __save_file_to_s3(file, filename):
    bucket = __get_bucket(region_name=REGION)
    bucket.upload_fileobj(
        Fileobj=file,
        Key=filename,
        ExtraArgs={'ACL': 'public-read'}
    )


def __get_file_from_s3(file_uuid, filename):
    bucket = __get_bucket(region_name=REGION)

    try:
        file = io.BytesIO()
        bucket.download_fileobj(Key=file_uuid, Fileobj=file)
        file.seek(0)
        return send_file(file, attachment_filename=filename, as_attachment=True)
    except Exception as e:
        return str(e)


def __get_bucket(region_name):
    access_key_id, access_key_secret, access_token = __get_secret()
    if access_key_id is None or access_key_secret is None:
        raise RuntimeError('No secrets are present!')

    session = __aws_session(access_key_id, access_key_secret, region_name)
    s3_resource = session.resource('s3')
    return s3_resource.Bucket('awsbasicstrainingbucket')


def __aws_session(access_key_id, access_key_secret, region_name='us-east-1'):
    return boto3.session.Session(aws_access_key_id=access_key_id,
                                 aws_secret_access_key=access_key_secret,
                                 region_name=region_name)


def __get_secret():
    session = boto3.Session()
    credentials = session.get_credentials()
    current_credentials = credentials.get_frozen_credentials()
    print(current_credentials.access_key)
    return current_credentials.access_key, current_credentials.secret_key, current_credentials.token
