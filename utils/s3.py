from pathlib import PurePath
from .path import get_path_without_root, get_root_from_path


def list_buckets(client):
    return client.list_buckets()


def list_objects(client, s3_location):
    return client.list_objects_v2(
        Bucket=get_root_from_path(s3_location),
        Prefix=get_path_without_root(s3_location)
    )


def bucket_exists(client, bucket_name):
    try:
        client.head_bucket(Bucket=bucket_name)
        return True
    except Exception:
        return False


def object_exists(client, bucket_name, object_location):
    return client.list_objects(
        Bucket=bucket_name,
        Prefix=object_location,
        MaxKeys=1
    )


def folder_exists(client, bucket_name, directory_location):
    return client.list_objects(
        Bucket=bucket_name,
        Prefix=directory_location,
        Delimiter="/",
        MaxKeys=1
    )


def create_folder(client, bucket_name, folder_location_key):
    return client.put_object(
        Bucket=bucket_name,
        Key=str(PurePath(folder_location_key)) + "/"
    )
