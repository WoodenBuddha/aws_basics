from ...main import db
from .model.subscribers import Subscriber
from  sqlalchemy.sql.expression import func


def save(subscriber):
    db.session.add(subscriber)
    db.session.commit()


def delete(subscriber):
    db.session.delete(subscriber)
    db.session.commit()


def find_by_email(email):
    subscriber = Subscriber.query.filter_by(email=email).first()
    return subscriber
