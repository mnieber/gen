import json
import os

import jinja2
from jinja2_ansible_filters import AnsibleCoreFiltersExtension
from moonleap.utils import chop


def to_nice_json(value):
    return json.dumps(value, sort_keys=False, indent=4, separators=(",", ": "))


def load_template(template_fn):
    with open(template_fn) as ifs:
        lines = [chop(x) for x in ifs.readlines()]

        state = "search loop"
        end_idx = len(lines)
        idx = len(lines) - 1

        while idx >= 0:
            line = lines[idx]

            if line.strip() == "":
                end_idx = idx

            if state == "search start":
                if line.strip().startswith(r"{% for") and line.strip().endswith(r"%}"):
                    lines.insert(idx + 1, "{% if loop.first %}")
                    state = "search loop"

            if state == "search loop":
                if line.strip() == r"{% body %}":
                    lines[idx] = r"{% endif %}"
                    lines.insert(end_idx, r"{% endfor %}")
                    state = "search start"

            idx -= 1

        new_text = os.linesep.join(lines)

        template_loader = jinja2.FunctionLoader(lambda fn: new_text)
        template_env = jinja2.Environment(
            loader=template_loader,
            extensions=[AnsibleCoreFiltersExtension],
            trim_blocks=True,
        )
        template_env.filters["to_nice_json"] = to_nice_json
        return template_env.get_template("tplt")
