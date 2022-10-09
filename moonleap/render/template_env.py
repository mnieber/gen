import os

import jinja2
from moonleap.render.transforms import get_transforms
from moonleap.utils import chop

_last_template = dict()


def print_last_template():
    print("Template: %s" % _last_template["fn"])
    print(os.linesep.join(_last_template["lines"]))


def load_template(template_fn):
    with open(template_fn) as ifs:
        lines = [chop(x) for x in ifs.readlines()]

    transformed_lines = lines
    for t in get_transforms():
        transformed_lines = t(transformed_lines, template_fn)

    _last_template["fn"] = template_fn
    _last_template["lines"] = [
        "%3d: %s" % (i + 1, transformed_lines[i]) for i in range(len(transformed_lines))
    ]

    return os.linesep.join(transformed_lines)


template_loader = jinja2.FunctionLoader(load_template)
template_env = jinja2.Environment(
    loader=template_loader,
    trim_blocks=True,
    lstrip_blocks=True,
    undefined=jinja2.StrictUndefined,
)


def get_template(fn):
    return template_env.get_template(str(fn))


def add_filter(name, f):
    template_env.filters[name] = f


def drop_filter(name):
    del template_env.filters[name]


def get_filter(name):
    return template_env.filters.get(name)
