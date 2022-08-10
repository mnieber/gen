import re

import ramda as R

end_tag = r"{% end_break_line %}"

# This transform removes the trailing slash from the last line in a block of "broken lines".
# It also counts how many lines in this block have a trailing slash, and removes the entire
# block if it has less than the required minimum number of lines with a trailing slash.


def _find_tag(text):
    regex = r"{% break_line min_lines=(?P<min_lines>[0-9]+) %}"
    matches = list(re.finditer(regex, text, re.MULTILINE))
    return bool(matches), int(matches[0].group("min_lines")) if matches else 0


def process_break_line(lines, template_fn=None):
    result = []
    for line in lines:
        result.extend(
            ["{% raw %}" + line + "{% endraw %}", ""]
            if _find_tag(line)[0] or line == end_tag
            else [line]
        )

    return result


def post_process_break_line(lines, template_fn=None):
    result = []
    breaking = False
    min_lines = 0
    total_line_count = 0
    broken_line_count = 0

    for line in lines:
        tag = _find_tag(line)

        if tag[0]:
            breaking = True
            min_lines = tag[1]
            total_line_count = 0
            broken_line_count = 0
            continue

        if end_tag in line:
            breaking = False
            prev_line = result[-1].rstrip() if len(result) else None
            if prev_line:
                if prev_line.endswith("\\"):
                    result[-1] = prev_line[:-1].rstrip()
                elif broken_line_count:
                    broken_line_count += 1

            if broken_line_count < min_lines:
                for i in range(total_line_count):
                    result.pop()

            continue

        if breaking:
            total_line_count += 1
            if line.rstrip().endswith("\\"):
                broken_line_count += 1

        result.append(line)

    return result
