from argparse import Namespace
from pathlib import Path

from jinja2 import Template
from moonleap.render.render_template import render_template
from moonleap.render.render_templates.create_render_helpers import create_render_helpers
from moonleap.session import get_session


def render_templates(templates_dir, write_file, output_path, context, helpers):
    # Get next render helpers. Note that the existing helpers are continued to be
    # used in case the new __moonleap__.py file does not define get_helpers.
    (
        get_helpers,
        get_meta_data_by_fn,
        get_contexts,
    ) = create_render_helpers(templates_dir)

    context_ns = Namespace(**context)
    if get_helpers:
        helpers = get_helpers(_=context_ns)

    # Check if we must skip the current template directory
    meta_data_by_fn = (
        get_meta_data_by_fn(_=context_ns, __=helpers) if get_meta_data_by_fn else {}
    )
    current_dir_meta_data = meta_data_by_fn.get(".", {})
    if not current_dir_meta_data.get("include", True):
        return

    def render_in_context(template_fn, prefix=True, default="__not_set__"):
        full_template_fn = templates_dir / template_fn if prefix else template_fn

        if not full_template_fn.exists():
            if default == "__not_set__":
                raise Exception(f"Template not found: {full_template_fn}")
            return None

        return render_template(
            full_template_fn,
            dict(settings=get_session().settings, _=context_ns, __=helpers),
        )

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
