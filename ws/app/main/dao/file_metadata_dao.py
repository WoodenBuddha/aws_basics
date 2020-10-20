from ...main import db
from .model.file_metadata import FileMetadata


def save(file_metadata):
    db.session.add(file_metadata)
    db.session.commit()


def find_by_filename(filename):
    file_metadata = FileMetadata.query.filter_by(filename=filename).first()
    return file_metadata

