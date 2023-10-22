import importlib
import sys
from argparse import Namespace
from pathlib import Path

from moonleap.render.render_template import render_template
from moonleap.session import get_session


def create_render_helpers(templates_dir, context, prev_helpers):
    if not Path(templates_dir).is_dir():
        raise Exception(f"{templates_dir} is not a directory")

    helpers = prev_helpers
    meta_data_by_fn = {}
    context_ns = Namespace(**context, render=None)
    helpers_fn = templates_dir / "__moonleap__.py"

    if helpers_fn.exists():
        _validate_render_helpers_module(helpers_fn)
        sys.path.insert(0, str(templates_dir))
        m = importlib.import_module("__moonleap__")
        importlib.reload(m)
        sys.path.pop(0)

        if hasattr(m, "get_helpers"):
            helpers = m.get_helpers(_=context_ns)

        if hasattr(m, "get_meta_data_by_fn"):
            meta_data_by_fn = m.get_meta_data_by_fn(_=context_ns, __=helpers)

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

    context_ns.render = render_in_context
    return helpers, render_in_context, meta_data_by_fn


def _validate_render_helpers_module(fn):
    # Note that we are forced to take a cumbersome approach to validate the
    # __moonleap__.py file. If we simply import it, then Python may use a cached
    # version of get_helpers from a different __moonleap__.py file. Therefore,
    # we read the file and check that it contains the function get_helpers.
    with open(fn) as f:
        if "def get_helpers" not in f.read():
            raise Exception(f"__moonleap__.py must define a function get_helpers: {fn}")
