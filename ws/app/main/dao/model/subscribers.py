from ... import db

class Subscriber(db.Model):
    """ FileMetadata Model for storing file related details """
    __tablename__ = "subscriber"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    phone = db.Column(db.String(255), nullable=True)
    email = db.Column(db.String(255), nullable=True)
    email_json = db.Column(db.String(255), nullable=True)
    application = db.Column(db.String(255), nullable=True)
    aws_lambda = db.Column(db.String(255), nullable=True)
    http = db.Column(db.String(255), nullable=True)
    https = db.Column(db.String(255), nullable=True)
    prioritized = db.Column(db.String(255), nullable=True)
    subscriber_arn = db.Column(db.String(255), nullable=False)
    timestamp = db.Column(db.DateTime)

    def __init__(self, email, arn, timestamp):
        self.email = email
        self.subscriber_arn = arn
        self.timestamp = timestamp