from boto3 import Session
from moto import mock_s3


@mock_s3
def test():
    session = Session(aws_access_key_id='dummy', aws_secret_access_key='dummy')
    s3_client = session.client('s3')
    s3_client.create_bucket(Bucket='dummy')
    s3_client.put_object(Bucket='dummy', Key='1.txt', Body=b'hello')
    response = s3_client.get_object(Bucket='dummy', Key='1.txt')
    body = response['Body'].read()
    assert body == b'hello'
