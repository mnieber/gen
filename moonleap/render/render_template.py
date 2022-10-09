import os

from moonleap.render.template_env import get_template, print_last_template
from moonleap.render.transforms import get_post_transforms


def render_template(template_fn, **kwargs):
    if template_fn.suffix == ".j2":
        try:
            content = get_template(template_fn).render(**kwargs)
        except Exception:
            print_last_template()
            raise

        lines = content.split(os.linesep)
        for post_transform in get_post_transforms():
            lines = post_transform(lines, template_fn)
        content = os.linesep.join(lines)
    else:
        try:
            with open(template_fn) as ifs:
                content = ifs.read()
        except UnicodeDecodeError:
            with open(template_fn, "rb") as ifs:
                content = ifs.read()

    return content
