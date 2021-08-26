import os
from pathlib import Path

from jinja2 import Template
from moonleap.render.template_env import template_env
from moonleap.session import get_session


def _resolve_output_fn(templates_path, resource, template_fn):
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
        else Template(template_fn.name).render(res=resource)
    )

    if name.endswith(".j2"):
        name = name[:-3]

    return _resolve_output_fn(templates_path, resource, template_fn.parent) / name


def render_templates(root_filename, location="templates", **kwargs):
    def render(resource, write_file, render_template):
        location_path = Path(root_filename).parent / (
            location(resource) if callable(location) else location
        )
        if location_path.is_dir():
            templates_path = location_path
            template_paths = templates_path.glob("**/*")
        else:
            templates_path = location_path.parent
            template_paths = [location_path]

        for template_fn in template_paths:
            if template_fn.suffix == ".fn":
                continue
            if not template_fn.is_dir():
                output_fn = Path(resource.merged_output_path) / _resolve_output_fn(
                    templates_path,
                    resource,
                    template_fn.relative_to(templates_path),
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
