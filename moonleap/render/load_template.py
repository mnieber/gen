import json
import os
import re

import jinja2
from jinja2_ansible_filters import AnsibleCoreFiltersExtension
from moonleap.utils import chop


def to_nice_json(value):
    return json.dumps(value, sort_keys=False, indent=4, separators=(",", ": "))


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


def load_template(template_fn):
    block = []
    blocks = []
    result = ""

    with open(template_fn) as ifs:
        lines = [x for x in ifs.readlines()]

        for line in lines:
            if not chop(line):
                blocks.append(block)
                block = []
            else:
                block.append(line)

        if block:
            blocks.append(block)

        for block in blocks:
            var, container = _find_loop_statement(os.linesep.join(block))
            if not var:
                result += os.linesep.join(block) + os.linesep
                continue

            result += "{% for " + var + " in " + container + " %}\n"
            result += "{% if loop.first %}\n"

            for block_line in block:
                if block_line.startswith(r"{% loop"):
                    result += "{% endif %}\n"
                    result += "{% if loop.first or not loop.last %}\n"
                elif block_line.startswith(r"{% endloop"):
                    result += "{% else %}\n"
                else:
                    expr, line = _find_onlyif_statement(block_line)
                    if expr:
                        result += "{% if " + expr + " %}\n"
                        result += line
                        result += "{% endif %}\n"
                    else:
                        result += line

            result += "{% endif %}\n"
            result += "{% endfor %}\n"
            result += os.linesep

        template_loader = jinja2.FunctionLoader(lambda fn: result)
        template_env = jinja2.Environment(
            loader=template_loader,
            extensions=[AnsibleCoreFiltersExtension],
            trim_blocks=True,
        )
        template_env.filters["to_nice_json"] = to_nice_json
        return template_env.get_template("tplt")
