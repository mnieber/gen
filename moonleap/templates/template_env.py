import io
import os

import jinja2
from moonleap.templates.transforms import get_transforms
from moonleap.utils import chop

_template_by_fn = dict()


def print_last_template(template_fn):
    print("Template: %s" % template_fn)
    print(os.linesep.join(_template_by_fn.get(str(template_fn), [])))


def load_template(template_fn):
    with open(template_fn) as ifs:
        return get_template_from_stream(ifs, template_fn)


def get_template_from_stream(ifs, template_fn=None):
    lines = [chop(x) for x in ifs.readlines()]

    transformed_lines = lines
    for t in get_transforms():
        transformed_lines = t(transformed_lines, template_fn)

    if template_fn:
        _template_by_fn[str(template_fn)] = [
            "%3d: %s" % (i + 1, transformed_lines[i])
            for i in range(len(transformed_lines))
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


def get_template_from_str(template_str, template_id=None):
    with io.StringIO(template_str) as ifs:
        return template_env.from_string(
            get_template_from_stream(ifs, template_fn=template_id)
        )


def add_filter(name, f):
    template_env.filters[name] = f


def drop_filter(name):
    del template_env.filters[name]


def get_filter(name):
    return template_env.filters.get(name)
