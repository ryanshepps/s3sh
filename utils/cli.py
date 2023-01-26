from .path import get_path_without_root, get_root_from_path


def get_flags(split_command):
    flags = []

    for arg in split_command:
        if arg[0] == "-":
            flags.append(arg)

    return flags


def get_args(split_command):
    args = []

    for arg in split_command:
        if arg[0] != "-":
            args.append(arg)

    return args


def format_buckets_list(buckets):
    formatted_buckets_list = ""

    if "Buckets" in buckets:
        for bucket in buckets["Buckets"]:
            formatted_buckets_list += "{}\t".format(bucket["Name"])

    return formatted_buckets_list


def format_objects_list(objects, s3_location, in_long_format):
    formatted_objects_list = ""

    if "Contents" in objects:
        already_printed_objects = []

        for object in objects["Contents"]:
            object_key_cur_dir_removed = object["Key"].replace(get_path_without_root(s3_location), "")
            top_level_object_key = get_root_from_path(object_key_cur_dir_removed)

            if "/" in object_key_cur_dir_removed:
                top_level_object_key += "/"

            if top_level_object_key not in already_printed_objects and top_level_object_key != ".":
                if in_long_format:
                    formatted_objects_list += "{}\t{}\t{}\n".format(
                        '1' if top_level_object_key.endswith("/") else object["Size"],
                        object["LastModified"].strftime("%b %d %H:%M"),
                        top_level_object_key,
                    )
                else:
                    formatted_objects_list += "{}\t".format(top_level_object_key)

                already_printed_objects.append(top_level_object_key)

    return formatted_objects_list
