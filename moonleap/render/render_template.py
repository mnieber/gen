import os

from moonleap.render.template_env import template_env
from moonleap.render.transforms import get_post_transforms


def render_template(template_fn, **kwargs):
    if template_fn.suffix == ".j2":
        template = template_env.get_template(str(template_fn))
        content = template.render(**kwargs)

        lines = content.split(os.linesep)
        for post_transform in get_post_transforms():
            lines = post_transform(lines)
        content = os.linesep.join(lines)
    else:
        try:
            with open(template_fn) as ifs:
                content = ifs.read()
        except UnicodeDecodeError:
            with open(template_fn, "rb") as ifs:
                content = ifs.read()

    return content
