import boto3
import os
import io
import json
import copy

DEFAULT_S3_BUCKET = 'aws-basics-module-target-from-app'
DEFAULT_REGION = 'eu-west-1'


def save_file_to_s3(file, filename):
    try:
        __save_file_to_bucket(file, filename, DEFAULT_REGION, DEFAULT_S3_BUCKET)
    except Exception as e:
        print(e)
        print('Trying to create bucket with name {}'.format(DEFAULT_S3_BUCKET))
        statusCode = invoke_bucket_creation_lambda(DEFAULT_S3_BUCKET)
        if statusCode == 200:
            print('Got here <-')
            __save_file_to_bucket(file, filename, DEFAULT_REGION, DEFAULT_S3_BUCKET)


def get_file_from_s3(file_uuid):
    return __get_file_from_bucket(file_uuid, DEFAULT_REGION, DEFAULT_S3_BUCKET)


def __save_file_to_bucket(file, filename, region, bucket_name):
    bucket = __get_bucket(region, bucket_name)
    bucket.upload_fileobj(
        Fileobj=file,
        Key=filename,
        ExtraArgs={'ACL': 'public-read'}
    )


def __get_file_from_bucket(file_uuid, region, bucket_name):
    bucket = __get_bucket(region, bucket_name)
    try:
        file = io.BytesIO()
        bucket.download_fileobj(Key=file_uuid, Fileobj=file)
        file.seek(0)
        return file
    except Exception as e:
        return str(e)


def __get_bucket(region_name, bucket_name='awsbasicstrainingbucket'):
    # access_key_id, access_key_secret, access_token = get_secret()
    # if access_key_id is None or access_key_secret is None:
    #     raise RuntimeError('No secrets are present!')
    #
    # session = __aws_session(access_key_id, access_key_secret, region_name)
    if boto3.resource('s3').Bucket(bucket_name) not in boto3.resource('s3').buckets.all():
        raise Exception('NoSuchBucket!')
    s3_resource = boto3.resource('s3')
    return s3_resource.Bucket(bucket_name)


def invoke_bucket_creation_lambda(name):
    lambda_arn = __get_s3_creation_lambda_arn()
    lambda_client = boto3.client('lambda', region_name=DEFAULT_REGION)
    payload = {'BucketName': name}
    print('Creating new S3 bucket with name: {}'.format(name))
    status = lambda_client.invoke(
        FunctionName=lambda_arn,
        LogType='None',
        Payload=json.dumps(payload)
    )
    return status['StatusCode']


def __get_s3_creation_lambda_arn():
    print('Looking for specified Lambda..')
    client = boto3.client('lambda', region_name=DEFAULT_REGION)
    funcs = client.list_functions()
    for func in funcs['Functions']:
        print(func['FunctionName'])
        if func['FunctionName'] == 'createS3BucketLambda':
            print("Found Lambda instance with name: {}".format(func['FunctionName']))
            return func['FunctionArn']
    raise Exception('No Lambda function found!\n', funcs['Functions'])


def __aws_session(access_key_id, access_key_secret, region_name='us-east-1'):
    return boto3.session.Session(aws_access_key_id=access_key_id,
                                 aws_secret_access_key=access_key_secret,
                                 region_name=region_name)


def get_secret():
    session = boto3.Session()
    credentials = session.get_credentials()
    # assumed_role_object = __assume_role()
    # credentials = assumed_role_object['Credentials']

    # current_credentials = credentials.get_frozen_credentials()

    # aws_access_key_id = credentials['AccessKeyId']
    # aws_secret_access_key=credentials['SecretAccessKey']
    # aws_session_token=credentials['SessionToken']
    #
    # aws_access_key_id = os.environ['ACCESS_KEY']
    # aws_secret_access_key = os.environ['ACCESS_SECRET']
    # aws_session_token = os.environ['TOKEN']

    # TODO: remove before push
    aws_access_key_id = 'AKIA2MM5XDIWXA2AJQG7'
    aws_secret_access_key = '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'
    aws_session_token = ''

    return aws_access_key_id, aws_secret_access_key, aws_session_token


def __assume_role():
    sts_client = boto3.client('sts')
    return sts_client.assume_role(
        RoleArn="arn:aws:iam::713832208941:role/ec2-s3-readwrite-role",
        RoleSessionName="AssumeRoleSession1"
    )