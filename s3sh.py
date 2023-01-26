#!/usr/bin/env python3

import os
import configparser
import boto3
import botocore
from s3commands import \
    create_bucket, list, locs3cp, \
    cwlocn, chlocn, delete_bucket, \
    s3delete, create_folder, \
    s3copy, s3loccp


commands = {
    "create_bucket": create_bucket,
    "delete_bucket": delete_bucket,
    "list": list,
    "locs3cp": locs3cp,
    "cwlocn": cwlocn,
    "s3delete": s3delete,
    "create_folder": create_folder,
    "s3copy": s3copy,
    "s3loccp": s3loccp
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

    s3_location = "/"

    while client is not None:
        command = input("S5 {}> ".format(s3_location))

        try:
            split_command = command.split(" ")

            if split_command[0] == "exit" or split_command[0] == "quit":
                break
            if split_command[0] == "chlocn":
                s3_location = chlocn(client, split_command, s3_location)
            elif split_command[0] in commands:
                return_message = commands[split_command[0]](client, split_command, s3_location)
                if return_message is not None:
                    print(return_message)
            else:
                os.system(command)
        except Exception as e:
            print("An unknwon error occurred while running your command: \n\t{}".format(e))


if "__main__" == __name__:
    main()
