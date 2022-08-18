import importlib
import sys
from argparse import Namespace
from pathlib import Path

from jinja2 import Template
from moonleap.render.template_env import get_template
from moonleap.session import get_session
from moonleap.utils.ruamel_yaml import ruamel_yaml


def render_templates(
    templates_dir, write_file, render_template, output_path, context, helpers
):
    if not Path(templates_dir).is_dir():
        raise Exception(f"{templates_dir} is not a directory")

    next_helpers, meta_data_by_fn, skip = _load_moonleap_data(templates_dir, context)
    if skip:
        return

    helpers = next_helpers or helpers

    # create output directory
    write_file(output_path, content="", is_dir=True)

    # render templates
    for template_fn in Path(templates_dir).glob("*"):
        if (
            template_fn.name.startswith("__moonleap__")
            or template_fn.name == "__pycache__"
        ):
            continue

        print(template_fn)
        meta_data = meta_data_by_fn.get(template_fn.name, dict())
        if not meta_data.get("include", True):
            continue

        output_fn = _get_output_fn(output_path, template_fn, meta_data, context)
        if template_fn.is_dir():
            render_templates(
                template_fn,
                write_file,
                render_template,
                output_fn,
                context,
                helpers,
            )
        else:
            write_file(
                output_fn,
                content=render_template(
                    template_fn,
                    settings=get_session().settings,
                    _=context,
                    __=helpers,
                ),
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


def _load_moonleap_data(dir_fn, context):
    meta_data_by_fn = dict()
    meta_filename = dir_fn / "__moonleap__.j2"
    if meta_filename.exists():
        content = get_template(meta_filename).render(_=Namespace(**context))
        meta_data_by_fn = ruamel_yaml.load(content)
        for fn, meta_data in meta_data_by_fn.items():
            if not isinstance(meta_data.get("include", False), bool):
                raise Exception(
                    f"Invalid include value: "
                    + f"{meta_data.get('include')} for filename {fn} in {meta_filename}"
                )

    skip = not meta_data_by_fn.get(".", {}).get("include", True)
    helpers = None

    if not skip and (dir_fn / "__moonleap__.py").exists():
        sys.path.insert(0, str(dir_fn))
        m = importlib.import_module("__moonleap__")
        # TODO: if the new __moonleap__ file does not define get_helpers then
        # the one from the previously loaded __moonleap__ file will be used,
        # potentially crashing the code.
        importlib.reload(m)
        sys.path.pop(0)

        if hasattr(m, "get_helpers"):
            helpers = m.get_helpers(_=Namespace(**context))

    return helpers, meta_data_by_fn, skip
