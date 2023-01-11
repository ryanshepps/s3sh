#!/usr/bin/env python3

import sys
import os
import configparser
import boto3


def getAuthenticatedClient():
    aws_config = configparser.ConfigParser()
    aws_config.read('S5-S3.conf')
    return boto3.client(
        's3',
        aws_access_key_id=aws_config.get('default', 'aws_access_key_id'),
        aws_secret_access_key=aws_config.get('default', 'aws_secret_access_key')
    )


def main():
    print("Welcome to AWS S3 Storage Shell (S5)")

    client = getAuthenticatedClient()

    if client is None:
        print("You could not be connected to your S3 storage")
        print("Please review procedures for authenticating your account on AWS S3")
        sys.exit()
    else:
        print("You are now connected to your S3 storage")

    while True:
        command = input("S5> ")
        if command == "exit":
            break
        else:
            os.system(command)


if "__main__" == __name__:
    main()
