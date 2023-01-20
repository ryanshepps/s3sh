import unittest
from utils.cli import get_flags


class GetFlags(unittest.TestCase):
    def test_should_return_all_flags_from_split_command(self):
        mock_split_command = ["command", "-f", "file", "-s", "-t", "--tree", "test"]
        expected_flags = ["-f", "-s", "-t", "--tree"]

        flags = get_flags(mock_split_command)

        self.assertEqual(flags, expected_flags)
