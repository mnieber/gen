import os

import ramda as R
from moonleap.session import get_session
from titan.dodo_pkg.layer import LayerConfig


def get(project):
    settings = get_session().settings
    default_base_dir = R.path_or(None, ["references", "src"])(settings)
    base_dir = settings.get("code_workspaces_dir", default_base_dir)

    if not base_dir:
        return None

    code_workspace_fn = os.path.join(base_dir, f"{project.name_snake}.code-workspace")

    def inner():
        return dict(ROOT=dict(aliases=dict(code=f"exec 'code {code_workspace_fn}'")))

    return LayerConfig(lambda x: inner())
