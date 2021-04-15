import re

from moonleap.utils.case import title0


def _find_magic_with_statement(text):
    regex = r"{% magic_with (?P<var>[A-Za-z0-9_\.\|]+) as (?P<as>.+)\s* %}"
    matches = list(re.finditer(regex, text, re.MULTILINE))
    return (
        (
            matches[0].group("var"),
            matches[0].group("as"),
        )
        if matches
        else (None, None)
    )


def process_magic_with(lines):
    result = []
    vars = []
    for block_line in lines:
        var, as_ = _find_magic_with_statement(block_line)
        if var:
            vars.append((var, as_))
            continue

        if "{% end_magic_with %}" in block_line:
            vars.pop()
            continue

        x = block_line
        for var, as_ in vars:
            x = x.replace(as_ + "s", "{{ " + var + "|plural }}")
            x = x.replace(title0(as_) + "s", "{{ " + var + "|plural|title0 }}")
            x = x.replace(as_, "{{ " + var + " }}")
            x = x.replace(title0(as_), "{{ " + var + "|title0 }}")

            x = x.replace("{{{", "{{ '{' }}{{")
            x = x.replace("}}}", "{{ '}' }}}}")

        result.append(x)

    return result
