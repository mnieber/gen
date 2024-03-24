import os
from pathlib import Path

from moonleap.templates.template_env import (
    get_template,
    get_template_from_str,
    print_last_template,
)
from moonleap.templates.transforms import get_post_transforms


def render_template(template_fn, context, template_str=None):
    if Path(template_fn).suffix == ".j2":
        try:
            tpl = (
                get_template_from_str(template_str, template_fn)
                if template_str
                else get_template(template_fn)
            )
            content = tpl.render(context)
        except Exception:
            print_last_template(template_fn)
            raise

        lines = content.split(os.linesep)
        for post_transform in get_post_transforms():
            lines = post_transform(lines, template_fn)
        content = os.linesep.join(lines)
    else:
        if template_str:
            content = template_str
        else:
            try:
                with open(template_fn) as ifs:
                    content = ifs.read()
            except UnicodeDecodeError:
                with open(template_fn, "rb") as ifs:
                    content = ifs.read()

    return content
