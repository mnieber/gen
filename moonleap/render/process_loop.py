import os
import re


def _find_loop_statement(block):
    regex_loop = (
        r"{% loop (?P<var>[A-Za-z_\.]+) (as (?P<as>.+)\s*)?in (?P<container>.+) %}"
    )
    matches = list(re.finditer(regex_loop, block, re.MULTILINE))
    return (
        (
            matches[0].group("var"),
            matches[0].group("container"),
        )
        if matches
        else (None, None)
    )


def _find_onlyif_statement(line):
    regex_loop = r"{% onlyif (?P<expr>[A-Za-z_\.]+) %}"
    matches = list(re.finditer(regex_loop, line, re.MULTILINE))

    return (
        (matches[0].group("expr"), line[: matches[0].start()] + os.linesep)
        if matches
        else (None, line)
    )


def process_loop(lines):
    block = []
    blocks = []
    result = []

    for line in lines:
        block.append(line)
        if not line:
            blocks.append(block)
            block = []

    if block:
        blocks.append(block)

    for block in blocks:
        block_text = os.linesep.join(block)

        var, container = _find_loop_statement(block_text)
        if not var:
            result.extend(block)
            continue

        has_final_var_usage = block_text.rfind(var) > block_text.rfind("{% endloop %}")
        result += [
            #
            "{% for " + var + " in " + container + " %}",
            "{% if loop.first %}",
        ]

        for block_line in block:
            if block_line.startswith(r"{% loop"):
                result += ["{% endif %}"]
                if has_final_var_usage:
                    result += ["{% if not loop.last %}"]
            elif block_line.startswith(r"{% endloop %}"):
                if has_final_var_usage:
                    result += ["{% else %}"]
            else:
                expr, line = _find_onlyif_statement(block_line)
                if expr:
                    result += [
                        #
                        "{% if " + expr + " %}",
                        line,
                        "{% endif %}",
                    ]
                else:
                    result += [line]

        if has_final_var_usage:
            result += ["{% endif %}"]
        result += ["{% endfor %}"]

    return result
