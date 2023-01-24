import re
import os
from pathlib import PurePath


def get_root_from_path(s3_path):
    bucket_name = None

    pure_path = str(PurePath(s3_path))
    split_path = pure_path.split("/")

    if split_path[0] == "":
        bucket_name = split_path[1]
    else:
        bucket_name = split_path[0]

    return bucket_name


def get_path_without_root(s3_path):
    split_s3_path = re.findall(r".*?/", s3_path)
    file_in_path = re.findall(r"[^/]+$", s3_path)

    root_removed_path = None
    if len(split_s3_path) == 0:  # Path is at root
        return ""
    elif split_s3_path[0] == "/":
        root_removed_path = split_s3_path[2:]

        if len(split_s3_path) > 1:
            root_removed_path += file_in_path
    else:
        root_removed_path = split_s3_path[1:]

    s3_file_path = "".join(root_removed_path)

    if split_s3_path[0] != "/" and file_in_path:
        s3_file_path += file_in_path[0]

    return s3_file_path


def create_relative_or_absolute_path(requested_path, current_path):
    if (requested_path[0] == "/"):
        return requested_path
    else:
        return current_path + requested_path


def get_file_from_path(path):
    return os.path.basename(path)
