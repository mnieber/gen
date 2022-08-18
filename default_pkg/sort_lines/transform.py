import re

end_sort_lines_tag = "{% end_sort_lines %}"


def _find_tag(text):
    regex = r"{% sort_lines %}"
    matches = list(re.finditer(regex, text, re.MULTILINE))
    return bool(matches)


def process_sort_lines(lines, template_fn=None):
    result = []
    for line in lines:
        result.extend(
            ["{% raw %}" + line + "{% endraw %}", ""]
            if _find_tag(line) or line == end_sort_lines_tag
            else [line]
        )
    return result


def post_process_sort_lines(lines, template_fn=None):
    result = []
    block = []
    is_sorting = False

    for line in lines:
        if _find_tag(line):
            is_sorting = True
            continue

        if line == end_sort_lines_tag:
            result.extend(sorted(block))
            block = []
            continue

        if is_sorting:
            block.append(line)
            continue

        result.append(line)

    return result
