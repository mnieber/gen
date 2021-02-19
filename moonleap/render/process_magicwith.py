import os
import re

from moonleap.utils import title


def _find_magicwith_statement(text):
    regex_loop = r"{% magicwith (?P<var>[A-Za-z_\.]+) as (?P<as>.+)\s* %}"
    matches = list(re.finditer(regex_loop, text, re.MULTILINE))
    return (
        (
            matches[0].group("var"),
            matches[0].group("as"),
        )
        if matches
        else (None, None)
    )


def process_magicwith(lines):
    result = []
    vars = []
    for block_line in lines:
        var, as_ = _find_magicwith_statement(block_line)
        if var:
            vars.append((var, as_))
            continue

        if "{% endmagicwith %}" in block_line:
            vars.pop()
            continue

        x = block_line
        for var, as_ in vars:
            x = x.replace(as_ + "s", "{{ " + var + "|plural }}")
            x = x.replace(title(as_) + "s", "{{ " + var + "|plural|title }}")
            x = x.replace(as_, "{{ " + var + " }}")
            x = x.replace(title(as_), "{{ " + var + "|title }}")

            x = x.replace("{{{", "{{ '{' }}{{")
            x = x.replace("}}}", "{{ '}' }}}}")

        result.append(x)

    return result
