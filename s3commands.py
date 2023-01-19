import os
import botocore
import re
from pathlib import PurePath


def __get_flags(split_command):
    flags = []

    for arg in split_command:
        if arg[0] == "-":
            flags.append(arg)

    return flags


def __get_args(split_command):
    args = []

    for arg in split_command:
        if arg[0] != "-":
            args.append(arg)

    return args


def __get_root_from_path(s3_path):
    bucket_name = None

    pure_path = str(PurePath(s3_path))
    split_path = pure_path.split("/")

    if split_path[0] == "":
        bucket_name = split_path[1]
    else:
        bucket_name = split_path[0]

    return bucket_name


def __get_path_without_root(s3_path):
    split_s3_path = re.findall(r".*?/", s3_path)
    file_in_path = re.findall(r"[^/]+$", s3_path)

    root_removed_path = None
    if split_s3_path[0] == "/":
        root_removed_path = split_s3_path[2:]
    else:
        root_removed_path = split_s3_path[1:]

    s3_file_path = "".join(root_removed_path)

    if file_in_path:
        s3_file_path += file_in_path[0]

    return s3_file_path


def create_bucket(client, split_command, s3_location):
    bucket_name = __get_root_from_path(split_command[1])

    try:
        client.create_bucket(Bucket=bucket_name)
    except botocore.exceptions.ClientError as e:
        return "Cannot create bucket: \n\t{}".format(e)


def list(client, split_command, s3_location):
    flags = __get_flags(split_command)
    args = __get_args(split_command)

    if "-l" in flags:
        print("list long format")
    else:
        if args[1:]:
            print("There are arguments... {} List from the relative file location.".format(args[1:]))
        else:
            # There are no arguments, so list the s3_location
            if s3_location == "/":  # List buckets
                buckets = client.list_buckets()
                for bucket in buckets["Buckets"]:
                    print("{}\t".format(bucket["Name"]), end="")
                print("")
            else:  # List objects
                objects = client.list_objects_v2(
                    Bucket=__get_root_from_path(s3_location),
                    Prefix=__get_path_without_root(s3_location)
                )

                if "Contents" in objects:
                    already_printed_objects = []

                    for object in objects["Contents"]:
                        object_key_cur_dir_removed = object["Key"].replace(__get_path_without_root(s3_location), "")
                        top_level_object_key = __get_root_from_path(object_key_cur_dir_removed)

                        if "/" in object_key_cur_dir_removed:
                            top_level_object_key += "/"

                        if top_level_object_key not in already_printed_objects and top_level_object_key != ".":
                            # Print object
                            print("{}\t".format(top_level_object_key), end="")
                            already_printed_objects.append(top_level_object_key)
                print("")


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
                Key=__get_path_without_root(s3_path) + os.path.basename(local_file.name),
                Bucket=__get_root_from_path(s3_path),
            )
        except botocore.exceptions.ClientError as e:
            return "Unsuccessful copy: \n\t{}".format(e)


def cwlocn(client, split_command, s3_location):
    print(s3_location)


def chlocn(client, split_command, s3_location):
    new_s3_location = s3_location

    split_requested_s3_path = str(PurePath(split_command[1])).split("/")
    try:
        current_s3_location = s3_location

        while len(split_requested_s3_path) > 0:
            if current_s3_location == "/":  # Changing location to a bucket
                bucket_name = split_requested_s3_path[0]
                client.head_bucket(Bucket=bucket_name)
                current_s3_location = "/" + bucket_name
            else:
                objects = client.list_objects(
                    Bucket=__get_root_from_path(current_s3_location),
                    Prefix=__get_path_without_root(s3_location) + split_requested_s3_path[0],
                    MaxKeys=1
                )

                if 'Contents' not in objects:
                    raise Exception("{} could not be found in {}".format(split_requested_s3_path[0], split_command[1]))
                else:
                    current_s3_location += "/" + split_requested_s3_path[0] + "/"

            split_requested_s3_path = split_requested_s3_path[1:]

        new_s3_location = str(PurePath(current_s3_location)) + "/"
    except botocore.exceptions.ClientError as e:
        print("There was an issue changing to that location. Check that the location exists.\n\t{}".format(e))
    except Exception as e:
        print("Unable to change to {}.\n\tError: {}.".format(new_s3_location, e))

    return new_s3_location
