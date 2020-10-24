import boto3
from datetime import datetime

from . import aws_service
from ..dao import subscriber_dao
from ..dao.model.subscribers import Subscriber

DEFAULT_TOPIC_NAME = 'PhotoUploadTopic'


def _get_sns_client():
    access, secret, _ = aws_service.get_secret()
    return boto3.client(
        "sns",
        aws_access_key_id=access,
        aws_secret_access_key=secret,
        region_name=aws_service.DEFAULT_REGION
    )


class SubscriptionService:
    def __init__(self):
        self.client = _get_sns_client()

    def __get_topic(self):
        root = self.client.list_topics()
        topics_list = root['Topics']
        for t in topics_list:
            topic_arn = t['TopicArn']
            if DEFAULT_TOPIC_NAME in topic_arn:
                return topic_arn
        return None

    def subscribe(self, validated_email):
        topic_arn = self.__get_topic()
        subscription_arn = self.client.subscribe(
            TopicArn=topic_arn,
            Protocol='email',
            Endpoint=validated_email,
            ReturnSubscriptionArn=True
        )

        subscriber = Subscriber(validated_email, subscription_arn['SubscriptionArn'], datetime.now())
        subscriber_dao.save(subscriber)
        print("Subscription completed for: [{}]".format(validated_email))

    def unsubscribe(self, validated_email):
        subscriber = subscriber_dao.find_by_email(validated_email)

        self.client.unsubscribe(
            SubscriptionArn=subscriber.subscriber_arn
        )

        subscriber_dao.delete(subscriber)
        print("Unsubscription completed for: [{}]".format(validated_email))

    def publish(self):
        topic_arn = self.__get_topic()
        self.client.publish(Message="Good news everyone! There is more photos on your S3 :)))", TopicArn=topic_arn)
