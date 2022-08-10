import os
import re

import ramda as R

end_trim_newlines_tag = "{% end_trim_newlines %}"


def _find_trim_tag(text):
    regex = r"{% trim_newlines keep=(?P<keep>[0-9]+) %}"
    matches = list(re.finditer(regex, text, re.MULTILINE))
    return int(matches[0].group("keep")) if matches else None


def process_trim_newlines(lines, template_fn=None):
    result = []
    for line in lines:
        result.extend(
            ["{% raw %}" + line + "{% endraw %}", ""]
            if _find_trim_tag(line) is not None or line == end_trim_newlines_tag
            else [line]
        )
    return result


def post_process_trim_newlines(lines, template_fn=None):
    result = []
    trimming_keep = None
    no_content_yet = True
    empty_line_count = 0
    count = 0

    for line in lines:
        new_trimming_keep = _find_trim_tag(line)

        if new_trimming_keep is not None:
            if trimming_keep is not None:
                raise Exception("Can't have nested trimming tags")

            count += 1
            trimming_keep = new_trimming_keep
            continue

        if line == end_trim_newlines_tag:
            count -= 1
            trimming_keep = None
            empty_line_count = 0
            continue

        if line.strip() == "":
            if trimming_keep and (empty_line_count >= trimming_keep or no_content_yet):
                continue
            else:
                empty_line_count += 1
        else:
            no_content_yet = False
            empty_line_count = 0

        result.append(line)

    if count != 0:
        raise Exception(
            "{% trim_newlines %} not matched equally by {% end_trim_newlines %}"
        )

    return result
