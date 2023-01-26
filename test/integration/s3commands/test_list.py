import unittest
from unittest.mock import patch
from s3commands import \
    list


@patch("s3commands.list_objects")
class List(unittest.TestCase):
    def test_should_list_relative_dir_locations(
        self,
        mock_list_objects,
    ):
        mock_list_objects.return_value = {
            "Contents": [
                {
                    "Key": "/test_dir/big_test/test_file.py"
                }
            ]
        }

        mock_split_command = ["list", "big_test/"]
        mock_s3_location = "/test-bucket/test_dir/"
        expected_result = "test_file.py/\t"  # This is wrong for some reason

        result = list(None, mock_split_command, mock_s3_location)

        self.assertEqual(result, expected_result)
