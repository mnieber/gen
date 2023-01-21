import re


def split_non_empty(x):
    if not x:
        return []
    return [x.strip() for x in split_by_commas(x)]


def split_by_commas(s):
    lst = list()
    brackets = 0
    word = ""
    for c in s:
        if c == "[":
            brackets += 1
        elif c == "]":
            if brackets > 0:
                brackets -= 1
        elif c == "," and not brackets:
            lst.append(word)
            word = ""
            continue
        word += c
    lst.append(word)
    return lst
