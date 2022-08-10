import re


def _find_shortcut_if__statement(text):
    regex = r"{% \?\? (?P<what>[^%]+) %}"
    matches = list(re.finditer(regex, text, re.MULTILINE))
    return matches[0].group("what") if matches else None


def process_shortcut_if(lines, template_fn):
    result = []
    for block_line in lines:
        shortcut_if = _find_shortcut_if__statement(block_line)
        if shortcut_if:
            block_line = block_line.replace(
                "{% ?? " + shortcut_if + " %}",
                "{% if " + shortcut_if + " %}{% endif %}",
            )

        result.append(block_line)

    return result
