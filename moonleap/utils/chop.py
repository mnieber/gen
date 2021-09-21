def chop_postfix(x, postfix):
    if x.endswith(postfix):
        return x[: -len(postfix)]
    return x
