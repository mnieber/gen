def chop_postfix(x, postfix):
    if x.endswith(postfix):
        return x[: -len(postfix)]
    return x


def chop_prefix(x, prefix):
    if x.startswith(prefix):
        return x[len(prefix) :]
    return x
