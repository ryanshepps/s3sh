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
