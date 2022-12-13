import logging
import boto3
from botocore.exceptions import ClientError

AWS_REGION = 'us-east-1'
ACCESS_ID = 'AKIAVGGBPRX5IMJRKD75'
ACCESS_KEY = 'F1jL2fh9ja0qqWwSAol8sipknDB3D5adhmAX2+md'
TOPIC_ARN = "arn:aws:sns:us-east-1:356888055290:warriors_sns"

logger = logging.getLogger()
sns_client = boto3.client('sns', region_name=AWS_REGION,
                          aws_access_key_id=ACCESS_ID,
                          aws_secret_access_key=ACCESS_KEY)

# logger config
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s: %(levelname)s: %(message)s')


def publish_message(message, subject):
    try:
        response = sns_client.publish(
            TopicArn=TOPIC_ARN,
            Message=message,
            Subject=subject,
        )['MessageId']

    except ClientError:
        logger.exception(f'Could not publish message to the topic.')
        raise
    else:
        return response


def list_topics():
    try:
        paginator = sns_client.get_paginator('list_topics')
        page_iterator = paginator.paginate().build_full_result()
        topics_list = []

        for page in page_iterator['Topics']:
            topics_list.append(page['TopicArn'])
    except ClientError:
        logger.exception(f'Could not list SNS topics.')
        raise
    else:
        return topics_list
