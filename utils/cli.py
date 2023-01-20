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
