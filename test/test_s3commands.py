import unittest
from s3commands import \
    __get_flags as get_flags, \
    __get_path_without_root as get_path_without_root


class __get_flags(unittest.TestCase):
    def test_should_return_all_flags_from_split_command(self):
        mock_split_command = ["command", "-f", "file", "-s", "-t", "--tree", "test"]
        expected_flags = ["-f", "-s", "-t", "--tree"]

        flags = get_flags(mock_split_command)

        self.assertEqual(flags, expected_flags)


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
        expected_path = "bigtest.py"

        resulting_path = get_path_without_root(mock_path)

        self.assertEqual(resulting_path, expected_path)
