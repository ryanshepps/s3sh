import unittest
from pathlib import PurePath
from utils.path import \
    get_path_without_root, \
    create_relative_or_absolute_path


class __get_path_without_root(unittest.TestCase):
    def test_should_return_root_removed_when_more_than_one_consecutive_slash(self):
        mock_path = "test-bucket5807738/test_dir//big_test/"
        expected_path = "test_dir//big_test/"

        resulting_path = get_path_without_root(mock_path)

        self.assertEqual(resulting_path, expected_path)

    def test_should_return_root_removed_when_slash_at_beginning_of_path(self):
        mock_path = "/test-bucket5807738/test_dir/big_test/"
        expected_path = "test_dir/big_test/"

        resulting_path = get_path_without_root(mock_path)

        self.assertEqual(resulting_path, expected_path)

    def test_should_return_file_when_file_is_in_root(self):
        mock_path = "test-bucket5807738/bigtest.py"
        mock_path2 = "/test-bucket5807738/bigtest.py"
        expected_path = "bigtest.py"

        resulting_path = get_path_without_root(mock_path)
        resulting_path2 = get_path_without_root(mock_path2)

        self.assertEqual(resulting_path, expected_path)
        self.assertEqual(resulting_path2, expected_path)

    def test_should_return_empty_string_when_path_is_root(self):
        mock_path = "/test-bucket5807738"
        mock_path2 = "test-bucket5807738"
        expected_path = ""

        resulting_path = get_path_without_root(mock_path)
        resulting_path2 = get_path_without_root(mock_path2)

        self.assertEqual(resulting_path, expected_path)
        self.assertEqual(resulting_path2, expected_path)


class CreateRelativeOrAbsolutePath(unittest.TestCase):
    def test_should_return_absolute_path_when_slash_at_beginning_of_path(self):
        mock_requested_path = "/test/path/yeah/"
        mock_current_path = "/s3/location/yeah/"

        resulting_path = create_relative_or_absolute_path(mock_requested_path, mock_current_path)

        self.assertEqual(resulting_path, mock_requested_path)

    def test_should_return_relative_path_when_no_slash_at_beginning_of_path(self):
        mock_requested_path = "test/path/yeah/"
        mock_current_path = "/s3/location/yeah/"

        resulting_path = create_relative_or_absolute_path(mock_requested_path, mock_current_path)

        self.assertEqual(resulting_path, str(PurePath(mock_requested_path + mock_current_path)))
