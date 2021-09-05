import os
import re

import ramda as R

end_trim_newlines_tag = "{% end_trim_newlines %}"


def _find_trim_tag(text):
    regex = r"{% trim_newlines keep=(?P<keep>[0-9]+) %}"
    matches = list(re.finditer(regex, text, re.MULTILINE))
    return int(matches[0].group("keep")) if matches else None


def process_trim_newlines(lines):
    def t(x):
        keep = _find_trim_tag(x)
        has_tag = x == end_trim_newlines_tag or keep is not None

        return ("{% raw %}" + x + "{% endraw %}" + os.linesep) if has_tag else x

    return R.map(t, lines)


def post_process_trim_newlines(lines):
    result = []
    trimming = False
    trimming_keep = None
    empty_line_count = 0
    count = 0

    for line in lines:
        keep = _find_trim_tag(line)

        if keep is not None:
            count += 1
            trimming = True
            trimming_keep = keep
            empty_line_count = 0
            continue

        if line == end_trim_newlines_tag:
            count -= 1
            trimming = False
            trimming_keep = None
            continue

        if line.strip() == "":
            if trimming and empty_line_count >= trimming_keep:
                continue
            else:
                empty_line_count += 1
        else:
            empty_line_count = 0

        result.append(line)

    if count != 0:
        raise Exception(
            "{% trim_newlines %} not matched equally by {% end_trim_newlines %}"
        )

    return result
