import re

from moonleap.utils.case import l0, sn, u0


def _find_magic_with_statement(text):
    regex = r"{% magic_with (?P<as>.+)\s* \= (?P<var_name>[A-Za-z0-9_\,\ \[\]\.\\(\)\"|]+) %}"
    matches = list(re.finditer(regex, text, re.MULTILINE))
    return (
        (
            matches[0].group("var_name"),
            matches[0].group("as"),
        )
        if matches
        else (None, None)
    )


def process_magic_with(lines, template_fn=None):
    result = []
    var_names = []
    for block_line in lines:
        var_name, as_ = _find_magic_with_statement(block_line)

        if var_name:
            var_names.append((var_name, as_))
            continue

        if "{% end_magic_with %}" in block_line:
            var_names.pop()
            continue

        x = block_line
        for var_name, as_ in reversed(var_names):
            char0 = as_[0]
            starts_low = char0.lower() == char0
            change0, change0_str = (u0, "u0") if starts_low else (l0, "l0")

            x = x.replace(as_ + "s", "{{ " + var_name + "|plural }}")
            x = x.replace(sn(as_) + "s", "{{ " + var_name + "|sn|plural }}")

            x = x.replace(
                change0(as_) + "s", "{{ " + var_name + "|plural|%s }}" % change0_str
            )
            x = x.replace(
                change0(sn(as_)) + "s",
                "{{ " + var_name + "|sn|plural|%s }}" % change0_str,
            )

            x = x.replace(as_, "{{ " + var_name + " }}")
            x = x.replace(sn(as_), "{{ " + var_name + "|sn }}")

            x = x.replace(change0(as_), "{{ " + var_name + "|%s }}" % change0_str)
            x = x.replace(
                change0(sn(as_)), "{{ " + var_name + "|sn|%s }}" % change0_str
            )

            x = x.replace("{{{", "{{ '{' }}{{")
            x = x.replace("}}}", "}}{{ '}' }}")

        result.append(x)

    return result
