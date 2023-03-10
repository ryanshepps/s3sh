import unittest
from unittest.mock import patch
from s3commands import \
    chlocn


@patch("s3commands.bucket_exists")
@patch("s3commands.folder_exists")
class Chlocn(unittest.TestCase):

    def test_should_chlocn_to_different_bucket_when_aboslute_path_provided(
        self,
        mock_folder_exists,
        mock_bucket_exists,
    ):
        mock_bucket_exists.return_value = True
        mock_folder_exists.return_value = {
            "CommonPrefixes": ["another_test_dir/"]
        }

        mock_split_command = ["chlocn", "/test-bucket/test_dir/"]
        mock_s3_location = "/random-bucket/another_test_dir/"
        expected_result = "/test-bucket/test_dir/"

        result = chlocn(None, mock_split_command, mock_s3_location)

        self.assertEqual(result, expected_result)

    def test_should_chlocn_to_root_when_slash_provided(
        self,
        mock_folder_exists,
        mock_bucket_exists
    ):
        mock_bucket_exists.return_value = True
        mock_folder_exists.return_value = {
            "CommonPrefixes": ["another_test_dir/"]
        }

        mock_split_command = ["chlocn", "/"]
        mock_s3_location = "/random-bucket/another_test_dir/"
        expected_result = "/"

        result = chlocn(None, mock_split_command, mock_s3_location)

        self.assertEqual(result, expected_result)

    def test_should_chlocn_to_root_when_tilde_provided(
        self,
        mock_folder_exists,
        mock_bucket_exists
    ):
        mock_bucket_exists.return_value = True
        mock_folder_exists.return_value = {
            "CommonPrefixes": ["another_test_dir/"]
        }

        mock_split_command = ["chlocn", "~"]
        mock_s3_location = "/random-bucket/another_test_dir/"
        expected_result = "/"

        result = chlocn(None, mock_split_command, mock_s3_location)

        self.assertEqual(result, expected_result)

    def test_should_change_to_relative_path_when_relative_path_provided(
        self,
        mock_folder_exists,
        mock_bucket_exists
    ):
        mock_bucket_exists.return_value = True
        mock_folder_exists.return_value = {
            "CommonPrefixes": ["another_test_dir/"]
        }

        mock_split_command = ["chlocn", "another_test_dir/yeah/"]
        mock_s3_location = "/random-bucket/test_dir/"
        expected_result = "/random-bucket/test_dir/another_test_dir/yeah/"

        result = chlocn(None, mock_split_command, mock_s3_location)

        self.assertEqual(result, expected_result)

    def test_should_return_to_root_when_two_dots_provided_and_s3_location_is_one_level_deep(
        self,
        mock_folder_exists,
        mock_bucket_exists
    ):

        mock_split_command = ["chlocn", ".."]
        mock_s3_location = "/random-bucket/"
        expected_result = "/"

        result = chlocn(None, mock_split_command, mock_s3_location)

        self.assertEqual(result, expected_result)
