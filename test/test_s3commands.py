import unittest
from s3commands import \
    __get_flags as get_flags, \
    create_bucket
import boto3
from botocore.stub import Stubber

class __get_flags(unittest.TestCase):
    def test_should_return_all_flags_from_split_command(self):
        mock_split_command = ["command", "-f", "file", "-s", "-t", "--tree", "test"]
        expected_flags = ["-f", "-s", "-t", "--tree"]

        flags = get_flags(mock_split_command)

        self.assertEqual(flags, expected_flags)

class create_bucket(unittest.TestCase):
    def setUp(self):
        self.mock_client = boto3.client('s3')
        self.stubber = Stubber(self.mock_client)

    def test_should_create_bucket_when_slash_in_bucket_name(self):
        mock_split_command = "create_bucket /mock-bucket-name"

        result = create_bucket(self.mock_client, mock_split_command)
        
        self.assertIsNone()