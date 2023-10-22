import importlib
import sys
from pathlib import Path


def create_render_helpers(templates_dir):
    if not Path(templates_dir).is_dir():
        raise Exception(f"{templates_dir} is not a directory")

    get_helpers = None
    get_meta_data_by_fn = None
    get_contexts = None

    helpers_fn = Path(templates_dir) / "__moonleap__.py"
    if helpers_fn.exists():
        source_code = _get_moonleap_py_source(helpers_fn)
        sys.path.insert(0, str(templates_dir))
        m = importlib.import_module("__moonleap__")
        importlib.reload(m)
        sys.path.pop(0)

        if hasattr(m, "get_helpers") and "def get_helpers" in source_code:
            get_helpers = m.get_helpers

        if hasattr(m, "get_contexts") and "def get_contexts" in source_code:
            get_contexts = m.get_contexts

        if (
            hasattr(m, "get_meta_data_by_fn")
            and "def get_meta_data_by_fn" in source_code
        ):
            get_meta_data_by_fn = m.get_meta_data_by_fn

    return get_helpers, get_meta_data_by_fn, get_contexts


def _get_moonleap_py_source(fn):
    with open(fn) as f:
        return f.read()
