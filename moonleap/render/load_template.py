import os

import jinja2
from jinja2_ansible_filters import AnsibleCoreFiltersExtension
from moonleap.utils import chop


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

        templateLoader = jinja2.FunctionLoader(lambda fn: new_text)
        templateEnv = jinja2.Environment(
            loader=templateLoader,
            extensions=[AnsibleCoreFiltersExtension],
            trim_blocks=True,
        )
        return templateEnv.get_template("tplt")
