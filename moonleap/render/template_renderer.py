import os
from pathlib import Path

from jinja2 import Template
from moonleap.render.template_env import template_env
from moonleap.session import get_session


def _resolve_output_fn(templates_path, resource, template_fn, **kwargs):
    if str(template_fn) == ".":
        return template_fn

    meta_filename = str(templates_path / template_fn) + ".fn"
    name = (
        (
            template_env.get_template(meta_filename)
            .render(res=resource)
            .split(os.linesep)[0]
        )
        if Path(meta_filename).exists()
        else Template(template_fn.name).render(res=resource, **kwargs)
    )

    if name.endswith(".j2"):
        name = name[:-3]

    return _resolve_output_fn(templates_path, resource, template_fn.parent) / name


def render_templates(template_path, **kwargs):
    def render(resource, write_file, render_template):
        expanded_template_path = Path(
            template_path(resource) if callable(template_path) else template_path
        )

        if expanded_template_path.is_dir():
            templates_dir = expanded_template_path
            template_paths = expanded_template_path.glob("**/*")
        else:
            templates_dir = expanded_template_path.parent
            template_paths = [expanded_template_path]

        for template_fn in template_paths:
            if template_fn.suffix == ".fn":
                continue
            if not template_fn.is_dir():
                output_fn = Path(resource.merged_output_path) / _resolve_output_fn(
                    templates_dir,
                    resource,
                    template_fn.relative_to(templates_dir),
                    **kwargs,
                )
                write_file(
                    output_fn,
                    render_template(
                        resource,
                        template_fn,
                        settings=get_session().settings,
                        **kwargs,
                    ),
                )

    return render
