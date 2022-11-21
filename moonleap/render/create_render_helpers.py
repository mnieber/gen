import importlib
import sys
from argparse import Namespace
from pathlib import Path

from moonleap.session import get_session


def create_render_helpers(templates_dir, context, render_template, prev_helpers):
    if not Path(templates_dir).is_dir():
        raise Exception(f"{templates_dir} is not a directory")

    helpers = prev_helpers
    context_ns = Namespace(**context, render=None)

    if (templates_dir / "__moonleap__.py").exists():
        sys.path.insert(0, str(templates_dir))
        m = importlib.import_module("__moonleap__")
        # TODO: if the new __moonleap__ file does not define get_helpers then
        # the one from the previously loaded __moonleap__ file will be used,
        # potentially crashing the code.
        importlib.reload(m)
        sys.path.pop(0)

        if hasattr(m, "get_helpers"):
            helpers = m.get_helpers(_=context_ns)

    def render_in_context(template_fn, prefix=True, default="__not_set__"):
        full_template_fn = templates_dir / template_fn if prefix else template_fn

        if not full_template_fn.exists():
            if default == "__not_set__":
                raise Exception(f"Template not found: {full_template_fn}")
            return None

        return render_template(
            full_template_fn,
            settings=get_session().settings,
            _=context_ns,
            __=helpers,
        )

    context_ns.render = render_in_context
    return helpers, render_in_context
