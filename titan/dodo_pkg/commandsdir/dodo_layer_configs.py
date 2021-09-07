from titan.dodo_pkg.layer import LayerConfig


def get(project):
    commands_dir_name = project.name + "_commands"
    return LayerConfig(
        dict(
            ROOT=dict(
                command_path=["${/ROOT/src_dir}/extra/" + commands_dir_name],
            ),
        )
    )
