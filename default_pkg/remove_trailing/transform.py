import re
from ctypes.wintypes import tagMSG

# This transform removes the trailing slash from the last line in a block of "broken lines".
# It also counts how many lines in this block have a trailing slash, and removes the entire
# block if it has less than the required minimum number of lines with a trailing slash.


def _find_tag(text):
    regex = r'{% remove_trailing suffix="(?P<suffix>.+)" %}'
    matches = list(re.finditer(regex, text, re.MULTILINE))
    suffix = matches[0].group("suffix") if matches else None
    if suffix == "__backslash__":
        suffix = "\\"
    return bool(matches), suffix


def process_remove_trailing(lines, template_fn=None):
    result = []
    for line in lines:
        tag, suffix = _find_tag(line)
        result.extend(["{% raw %}" + line + "{% endraw %}", ""] if tag else [line])

    return result


def post_process_remove_trailing(lines, template_fn=None):
    result = []

    for line in lines:
        tag, suffix = _find_tag(line)
        if tag and suffix:
            if result[-1].rstrip().endswith(suffix):
                result[-1] = (result[-1][: -len(suffix)]).rstrip()
        else:
            result.append(line)

    return result
