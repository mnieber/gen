import os
from pathlib import Path

import ramda as R
from jinja2 import Template
from moonleap.render.template_env import template_env
from moonleap.session import get_session


def _resolve_output_fn(templates_path, template_fn, **kwargs):
    if str(template_fn) == ".":
        return template_fn

    meta_filename = str(templates_path / template_fn) + ".fn"
    name = (
        (template_env.get_template(meta_filename).render(**kwargs).split(os.linesep)[0])
        if Path(meta_filename).exists()
        else Template(template_fn.name).render(**kwargs)
    )

    if name.endswith(".j2"):
        name = name[:-3]

    return _resolve_output_fn(templates_path, template_fn.parent, **kwargs) / name


def render_templates(
    templates_dir, resource, write_file, render_template, output_path, get_context=None
):
    context_kwargs = dict(res=resource)
    if get_context:
        context_kwargs = R.merge(context_kwargs, get_context(resource))

    assert Path(templates_dir).is_dir()
    for template_fn in Path(templates_dir).glob("**/*"):
        if template_fn.suffix in (".fn", ".ml-meta"):
            continue

        output_fn = Path(output_path) / _resolve_output_fn(
            templates_dir, template_fn.relative_to(templates_dir), **context_kwargs
        )
        is_dir = template_fn.is_dir()

        write_file(
            output_fn,
            content=(
                ""
                if is_dir
                else render_template(
                    template_fn, settings=get_session().settings, **context_kwargs
                )
            ),
            is_dir=is_dir,
        )
