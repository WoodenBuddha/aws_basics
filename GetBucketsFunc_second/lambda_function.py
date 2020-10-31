import json
import urllib.parse
import boto3

s3 = boto3.resource('s3')

DEFAULT_BUCKET_NAME = 'aws-basics-module-target'

def lambda_handler(event, context):
    name = event['BucketName']
    if not name:
        name = DEFAULT_BUCKET_NAME
    print (event)
    try:
        return create_bucket(name)
    except Exception as e:
        print(e)
        raise e
        
        
        
def create_bucket(bucket_name, region='eu-west-1'):
    """Create an S3 bucket in a specified region

    :param bucket_name: Bucket to create
    :param region: String region to create bucket in, e.g., 'us-west-2'
    :return: True if bucket created, else False
    """

    try:
        if region is None:
            s3_client = boto3.client('s3')
            s3_client.create_bucket(Bucket=bucket_name)
        else:
            s3_client = boto3.client('s3', region_name=region)
            location = {'LocationConstraint': region}
            s3_client.create_bucket(Bucket=bucket_name,
                                    CreateBucketConfiguration=location)
    except ClientError as e:
        logging.error(e)
        return False
    return True