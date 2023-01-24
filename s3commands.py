import os
import botocore
from pathlib import PurePath
from utils.cli import \
    get_flags, \
    get_args, \
    format_buckets_list, \
    format_objects_list
from utils.path import \
    get_root_from_path, \
    get_path_without_root, \
    create_relative_or_absolute_path
from utils.s3 import \
    list_objects, \
    list_buckets, \
    bucket_exists, \
    object_exists, \
    folder_exists


def create_bucket(client, split_command, s3_location):
    bucket_name = get_root_from_path(split_command[1])

    try:
        client.create_bucket(Bucket=bucket_name)
    except botocore.exceptions.ClientError as e:
        return "Cannot create bucket: \n\t{}".format(e)


def delete_bucket(client, split_command, s3_location):
    bucket_name = get_root_from_path(split_command[1])

    try:
        client.delete_bucket(Bucket=bucket_name)
    except botocore.exceptions.ClientError as e:
        return "Cannot delete bucket: \n\t{}".format(e)


def list(client, split_command, s3_location):
    flags = get_flags(split_command)
    args = get_args(split_command)

    if "-l" in flags:
        print("list long format")
    else:
        if args[1:]:
            print("There are arguments... {} List from the relative file location.".format(args[1:]))
        else:
            # There are no arguments, so list the s3_location
            if s3_location == "/":
                buckets = list_buckets(client)
                return format_buckets_list(buckets)
            else:
                objects = list_objects(client, s3_location)
                return format_objects_list(objects, s3_location)


def locs3cp(client, split_command, s3_location):
    local_file = None
    s3_path = split_command[2]

    try:
        local_file = open(split_command[1], "rb")
    except Exception:
        return "Could not open file {}.\n\
\tCheck that it exists and that it is a format supported by S3" \
            .format(split_command[1])

    if local_file is not None:
        try:
            client.put_object(
                Body=local_file,
                Key=get_path_without_root(s3_path) + os.path.basename(local_file.name),
                Bucket=get_root_from_path(s3_path),
            )
        except botocore.exceptions.ClientError as e:
            return "Unsuccessful copy: \n\t{}".format(e)


def cwlocn(client, split_command, s3_location):
    print(s3_location)


def __change_bucket_location(client, s3_location, bucket_name):
    new_s3_location = s3_location

    if bucket_exists(client, bucket_name):
        new_s3_location = "/" + bucket_name
    else:
        raise Exception("Bucket does not exist")

    return new_s3_location


def __change_directory_location(client, current_s3_location, directory_name):
    if (directory_name == ".."):
        split_current_s3_location = current_s3_location.split("/")
        split_current_s3_location = split_current_s3_location[:-2]
        return "/".join(split_current_s3_location)

    response = folder_exists(
        client,
        get_root_from_path(current_s3_location),
        get_path_without_root(current_s3_location) + directory_name,
    )

    if "CommonPrefixes" not in response:
        raise Exception("{} is not a directory or it does not exist".format(
            directory_name,
        ))
    else:
        return current_s3_location + "/" + directory_name + "/"


def chlocn(client, split_command, s3_location):
    new_s3_location = s3_location

    if split_command[1][0] == "/":
        print("Not doing relative paths right now.")
    else:
        split_requested_s3_path = str(PurePath(split_command[1])).split("/")
        current_s3_location = s3_location

        try:
            while len(split_requested_s3_path) > 0:
                if current_s3_location == "/":
                    current_s3_location = __change_bucket_location(
                        client,
                        current_s3_location,
                        split_requested_s3_path[0]
                    )
                else:
                    current_s3_location = __change_directory_location(
                        client,
                        current_s3_location,
                        split_requested_s3_path[0]
                    )

                split_requested_s3_path = split_requested_s3_path[1:]

            new_s3_location = str(PurePath(current_s3_location)) + "/"
        except botocore.exceptions.ClientError as e:
            print("There was an issue changing to that location. Check that the location exists.\n\t{}".format(e))
        except Exception as e:
            print("Unable to change to {}.\n\tError: {}.".format(new_s3_location, e))

    return new_s3_location


def s3delete(client, split_command, s3_location):
    object_to_delete_path = create_relative_or_absolute_path(split_command[1], s3_location)

    if s3_location == "/" and object_to_delete_path[0] != "/":
        return "Cannot delete a relative object from outside a bucket"

    try:
        client.delete_object(
            Bucket=get_root_from_path(object_to_delete_path),
            Key=get_path_without_root(object_to_delete_path)
        )
    except botocore.exceptions.ClientError as e:
        return "Cannot delete {}. \n\t{}".format(object_to_delete_path, e)
