import os
import botocore

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

def __get_bucket_name(s3_path):
    return s3_path.split("/")[0]

def __get_s3_folder_path(s3_path):
    bucket_removed_path = s3_path.split("/")
    bucket_removed_path.pop(0)
    s3_file_path = "/".join(bucket_removed_path)
    
    if s3_file_path[len(s3_file_path) - 1] != "/":
        s3_file_path += "/"

    return s3_file_path
    

def create_bucket(client, split_command):
    bucket_name = split_command[1]

    try:
        client.create_bucket(Bucket=bucket_name)
    except botocore.exceptions.ClientError as e:
        return "Cannot create bucket: \n\t{}".format(e)


def list(client, split_command):
    flags = __get_flags(split_command)
    args = __get_args(split_command)

    if args[1] == "/":
        buckets = client.list_buckets()
        for bucket in buckets["Buckets"]:
            print("{}\t".format(bucket["Name"]))
    elif "-l" in flags:
        print("list long format")
    else:
        print("list short format")

def locs3cp(client, split_command):
    local_file = None
    s3_path = split_command[2]

    try: 
        local_file = open(split_command[1], "rb")
    except Exception as e:
        return "Could not open file {}.\n\
\tCheck that it exists and that it is a format supported by S3" \
            .format(split_command[1])

    if local_file is not None:
        try:
            client.put_object(
                Body=local_file,
                Key=__get_s3_folder_path(s3_path) + os.path.basename(local_file.name),
                Bucket=__get_bucket_name(s3_path),
            )
        except botocore.exceptions.ClientError as e:
            return "Unsuccessful copy: \n\t{}".format(e)
