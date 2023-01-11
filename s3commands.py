import botocore

def create_bucket(client, split_command):
    bucket_name = split_command[1]

    try:
        client.create_bucket(Bucket=bucket_name)
    except botocore.exceptions.ClientError as e:
        return "Cannot create bucket: \n\t{}".format(e)

    return "Success"