from argparse import Namespace
from pathlib import Path

from jinja2 import Template
from moonleap.render.render_templates.create_render_helpers import create_render_helpers


def render_templates(templates_dir, write_file, output_path, context, helpers):
    # Get next render helpers. Note that the existing helpers are continued to be
    # used in case the new __moonleap__.py file does not define get_helpers.
    helpers, render_in_context, meta_data_by_fn = create_render_helpers(
        templates_dir, context, prev_helpers=helpers
    )

    # Check if we must skip the current template directory
    current_dir_meta_data = meta_data_by_fn.get(".", {})
    if not current_dir_meta_data.get("include", True):
        return

    # create output directory
    write_file(output_path, content="", is_dir=True)

    # render templates
    for template_fn in Path(templates_dir).glob("*"):
        if (
            template_fn.name.startswith("__moonleap__")
            or template_fn.name == "__pycache__"
        ):
            continue

        meta_data = meta_data_by_fn.get(template_fn.name, dict())
        if not meta_data.get("include", True):
            continue

        output_fn = _get_output_fn(output_path, template_fn, meta_data, context)
        if template_fn.is_dir():
            render_templates(
                template_fn,
                write_file,
                output_fn,
                context,
                helpers,
            )
        else:
            write_file(
                output_fn,
                content=render_in_context(template_fn),
                is_dir=False,
            )


def _get_output_fn(output_path, template_fn, meta_data, context):
    name = (
        meta_data["name"]
        if "name" in meta_data
        else Template(template_fn.name).render(_=Namespace(**context))
    )

    if name.endswith(".j2"):
        name = name[:-3]

    return Path(output_path) / name
