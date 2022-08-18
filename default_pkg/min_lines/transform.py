import re

import ramda as R

end_tag = r"{% end_min_lines %}"

# This transform removes the trailing slash from the last line in a block of "broken lines".
# It also counts how many lines in this block have a trailing slash, and removes the entire
# block if it has less than the required minimum number of lines with a trailing slash.


def _find_tag(text):
    regex = r"{% min_lines count=(?P<count>[0-9]+) %}"
    matches = list(re.finditer(regex, text, re.MULTILINE))
    return bool(matches), int(matches[0].group("count")) if matches else 0


def process_min_lines(lines, template_fn=None):
    result = []
    for line in lines:
        result.extend(
            ["{% raw %}" + line + "{% endraw %}", ""]
            if _find_tag(line)[0] or line == end_tag
            else [line]
        )

    return result


def post_process_min_lines(lines, template_fn=None):
    result = []
    counting = False
    min_count = 0
    line_count = 0

    for line in lines:
        tag = _find_tag(line)

        if tag[0]:
            counting = True
            min_count = tag[1]
            line_count = 0
            continue

        if end_tag in line:
            counting = False
            if line_count < min_count:
                for i in range(line_count):
                    result.pop()

            continue

        if counting:
            line_count += 1

        result.append(line)

    return result
