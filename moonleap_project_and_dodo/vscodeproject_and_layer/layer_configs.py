import os

from moonleap.session import get_session
from moonleap_dodo.layer import LayerConfig


def get(project):
    settings = get_session().settings
    base_dir = settings.get("code_workspaces_dir", settings["references"]["src"])
    code_workspace_fn = os.path.join(base_dir, f"{project.name}.code-workspace")

    def inner():
        return dict(ROOT=dict(aliases=dict(code=f'exec "code {code_workspace_fn}"')))

    return LayerConfig(lambda x: inner())
