from moonleap import get_settings
from moonleap_dodo.layer import LayerConfig


def get(project):
    settings = get_settings()
    base_dir = settings.get("code_workspaces_dir", settings["target_dir"])

    def inner():
        return dict(
            ROOT=dict(
                aliases=dict(
                    code=f"exec -- code {base_dir}/"
                    + f"{project.name}.code-workspace --"
                )
            )
        )

    return LayerConfig(lambda x: inner())
