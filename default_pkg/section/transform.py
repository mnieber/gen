import re

end_tag = r"{% end_section %}"

# This transform removes the trailing slash from the last line in a block of "broken lines".
# It also counts how many lines in this block have a trailing slash, and removes the entire
# block if it has less than the required minimum number of lines with a trailing slash.


def _find_tag(text):
    regex = r"{% section (?P<name>.+) %}"
    matches = list(re.finditer(regex, text, re.MULTILINE))
    return bool(matches), matches[0].group("name") if matches else None


def process_section(lines, template_fn=None):
    result = []
    for line in lines:
        has_tag = _find_tag(line)[0] or line == end_tag
        result.extend(["{% raw %}" + line + "{% endraw %}", ""] if has_tag else [line])

    return result
