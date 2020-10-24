from ...main import db
from .model.file_metadata import FileMetadata
from  sqlalchemy.sql.expression import func


def save(file_metadata):
    db.session.add(file_metadata)
    db.session.commit()


def find_by_filename(filename):
    file_metadata = FileMetadata.query.filter_by(filename=filename).first()
    return file_metadata


def find_random():
    file_metadata = FileMetadata.query.order_by(func.random()).limit(1).first()
    return file_metadata