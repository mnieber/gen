def quote(x):
    return '"' + x + '"'


def quote_all(items):
    return [quote(item) for item in items]
