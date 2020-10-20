from ... import db


class FileMetadata(db.Model):
    """ FileMetadata Model for storing file related details """
    __tablename__ = "file"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    filename = db.Column(db.String(255), nullable=False)
    uuid = db.Column(db.String(255), nullable=False)
    extension = db.Column(db.String(255), nullable=False)
    timestamp = db.Column(db.DateTime)

    def __init__(self, filename, uuid, extension, timestamp):
        self.filename = filename
        self.uuid = uuid
        self.extension = extension
        self.timestamp = timestamp
