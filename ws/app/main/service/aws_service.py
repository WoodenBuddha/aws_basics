import boto3
import os
import io


DEFAULT_REGION = 'eu-west-1'


def save_file_to_s3(file, filename):
    bucket = __get_bucket(DEFAULT_REGION)
    bucket.upload_fileobj(
        Fileobj=file,
        Key=filename,
        ExtraArgs={'ACL': 'public-read'}
    )


def get_file_from_s3(file_uuid):
    bucket = __get_bucket(region_name=DEFAULT_REGION)

    try:
        file = io.BytesIO()
        bucket.download_fileobj(Key=file_uuid, Fileobj=file)
        file.seek(0)
        return file
    except Exception as e:
        return str(e)


def get_s3_bucket(region_name=DEFAULT_REGION):
    return __get_bucket(region_name)

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


def get_secret():
    session = boto3.Session()
    credentials = session.get_credentials()
    # assumed_role_object = __assume_role()
    # credentials = assumed_role_object['Credentials']

    # current_credentials = credentials.get_frozen_credentials()

    # aws_access_key_id = credentials['AccessKeyId']
    # aws_secret_access_key=credentials['SecretAccessKey']
    # aws_session_token=credentials['SessionToken']

    aws_access_key_id = os.environ['ACCESS_KEY']
    aws_secret_access_key = os.environ['ACCESS_SECRET']
    aws_session_token = os.environ['TOKEN']


    return aws_access_key_id, aws_secret_access_key, aws_session_token


def __assume_role():
    sts_client = boto3.client('sts')
    return sts_client.assume_role(
        RoleArn="arn:aws:iam::713832208941:role/ec2-s3-readwrite-role",
        RoleSessionName="AssumeRoleSession1"
    )