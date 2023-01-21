import re


def split_symbols(key):
    regex = r"([^\[]*)\[(.*)\]$"
    matches = list(re.finditer(regex, key, re.MULTILINE))
    symbols = ""

    if matches:
        if len(matches) > 1:
            raise Exception("Bad key syntax: " + key)
        key, symbols = matches[0].group(1), matches[0].group(2)
    return key, symbols
