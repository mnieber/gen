import json
import os
import re

import jinja2
from jinja2_ansible_filters import AnsibleCoreFiltersExtension
from moonleap.utils import chop


def to_nice_json(value):
    return json.dumps(value, sort_keys=False, indent=2, separators=(",", ": "))


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
            block_text = os.linesep.join(block)
            var, container = _find_loop_statement(block_text)
            if not var:
                result += "".join(block) + os.linesep
                continue

            has_final_var_usage = block_text.rfind(var) > block_text.rfind(
                "{% endloop %}"
            )
            result += "{% for " + var + " in " + container + " %}\n"
            result += "{% if loop.first %}\n"

            for block_line in block:
                if block_line.startswith(r"{% loop"):
                    result += "{% endif %}\n"
                    if has_final_var_usage:
                        result += "{% if not loop.last %}\n"
                elif block_line.startswith(r"{% endloop %}"):
                    if has_final_var_usage:
                        result += "{% else %}\n"
                else:
                    expr, line = _find_onlyif_statement(block_line)
                    if expr:
                        result += "{% if " + expr + " %}\n"
                        result += line
                        result += "{% endif %}\n"
                    else:
                        result += line

            if has_final_var_usage:
                result += "{% endif %}\n"
            result += "{% endfor %}\n"
            result += os.linesep

    return result


template_loader = jinja2.FunctionLoader(load_template)
template_env = jinja2.Environment(
    loader=template_loader,
    extensions=[AnsibleCoreFiltersExtension],
    trim_blocks=True,
)


def add_filter(name, f):
    template_env.filters[name] = f


template_env.filters["to_nice_json"] = to_nice_json
