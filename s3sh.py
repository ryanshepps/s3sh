#!/usr/bin/env python3

import os
import configparser
import boto3
import botocore
from s3commands import *


commands = {
    "create_bucket": create_bucket    
}


def getAuthenticatedClient():
    aws_config = configparser.ConfigParser()
    aws_config.read('S5-S3.conf')
    client = boto3.client(
        's3',
        aws_access_key_id=aws_config.get("default", "aws_access_key_id"),
        aws_secret_access_key=aws_config.get("default", "aws_secret_access_key")
    )

    try:
        client.list_buckets()
        print("You are now connected to your S3 storage")
        return client
    except botocore.exceptions.ClientError:
        print("You could not be connected to your S3 storage")
        print("Please review procedures for authenticating your account on AWS S3")
        return None


def main():
    print("Welcome to AWS S3 Storage Shell (S5)")

    client = getAuthenticatedClient()

    while client is not None:
        command = input("S5> ")
        if command == "exit":
            break
        else:
            split_command = command.split(" ")

            if split_command[0] in commands:
                try:
                    return_message = commands[split_command[0]](client, split_command)
                    print(return_message)
                except Exception as e:
                    print("An unknwon error occurred while running your command: \n\t{}".format(e))
            else:
                os.system(command)


if "__main__" == __name__:
    main()
