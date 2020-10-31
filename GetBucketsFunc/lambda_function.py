import json
import urllib.parse
import boto3

s3 = boto3.resource('s3')


def lambda_handler(event, context):
    for bucket in s3.buckets.all():
        print(bucket.name)
    
    try:
        response = [bucket.name for bucket in s3.buckets.all()]
        return json.dumps(response)
    except Exception as e:
        print(e)
        raise e