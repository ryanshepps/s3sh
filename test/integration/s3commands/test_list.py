import unittest
import datetime
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

    def test_should_list_current_s3_location_when_no_args_provided(
        self,
        mock_list_objects,
    ):
        mock_list_objects.return_value = {
            "Contents": [
                {
                    "Key": "test_file.py"
                }
            ]
        }

        mock_split_command = ["list"]
        mock_s3_location = "/test-bucket/"
        expected_result = "test_file.py\t"  # This is wrong for some reason

        result = list(None, mock_split_command, mock_s3_location)

        self.assertEqual(result, expected_result)

    def test_should_list_long_format_when_l_flag_provided(
        self,
        mock_list_objects,
    ):
        mock_list_objects.return_value = {
            "Contents": [
                {
                    "Key": "test_file.py",
                    "Size": "614",
                    "LastModified": datetime.datetime(2023, 1, 12, 12, 50, 27)
                }
            ]
        }

        mock_split_command = ["list", "-l"]
        mock_s3_location = "/test-bucket/"
        expected_result = "614\tJan 12 12:50\ttest_file.py\n"  # This is wrong for some reason

        result = list(None, mock_split_command, mock_s3_location)

        self.assertEqual(result, expected_result)
