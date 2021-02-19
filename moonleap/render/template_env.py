import json
import os

import jinja2
from jinja2_ansible_filters import AnsibleCoreFiltersExtension
from moonleap.render.transforms import transforms


def to_nice_json(value):
    return json.dumps(value, sort_keys=False, indent=2, separators=(",", ": "))


def load_template(template_fn):
    with open(template_fn) as ifs:
        lines = [x for x in ifs.readlines()]

    transformed_lines = lines
    for t in transforms:
        transformed_lines = t(transformed_lines)

    return "".join(transformed_lines) + os.linesep


template_loader = jinja2.FunctionLoader(load_template)
template_env = jinja2.Environment(
    loader=template_loader,
    extensions=[AnsibleCoreFiltersExtension],
    trim_blocks=True,
)


def add_filter(name, f):
    template_env.filters[name] = f


add_filter("to_nice_json", to_nice_json)
