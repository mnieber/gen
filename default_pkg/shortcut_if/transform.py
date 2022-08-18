import re


def _find_shortcut_if_statement(text):
    regex = r"{% \?\? (?P<what>[^%]+) %}"
    matches = list(re.finditer(regex, text, re.MULTILINE))
    return matches[0].group("what") if matches else None


def _find_shortcut_for_statement(text):
    regex = r"{% !! (?P<what>[^%]+) %}"
    matches = list(re.finditer(regex, text, re.MULTILINE))
    return matches[0].group("what") if matches else None


def process_shortcut_if(lines, template_fn):
    result = []
    for block_line in lines:
        shortcut_if = _find_shortcut_if_statement(block_line)
        if shortcut_if:
            block_line = block_line.replace(
                "{% ?? " + shortcut_if + " %}",
                "{% if " + shortcut_if + " %}{% endif %}",
            )

        shortcut_for = _find_shortcut_for_statement(block_line)
        if shortcut_for:
            block_line = block_line.replace(
                "{% !! " + shortcut_for + " %}",
                "{% for " + shortcut_for + " %}{% endfor %}",
            )

        result.append(block_line)

    return result
