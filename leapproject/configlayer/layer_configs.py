from leapdodo.layer import LayerConfig


def get_root_config():
    return LayerConfig(
        dict(
            ROOT=dict(
                command_path=["~/.dodo_commands/default_project/commands/*"],
                src_dir="${/ROOT/project_dir}/src",
                shared_config_dir=r"${/ROOT/src_dir}/extra/.dodo_commands",
                version="1.0.0",
            )
        )
    )
