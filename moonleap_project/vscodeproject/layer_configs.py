from moonleap.render.settings import load_settings_file
from moonleap.resources.outputpath.props import merged_output_path
from moonleap_dodo.layer import LayerConfig


def get(project):
    settings = load_settings_file()
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
