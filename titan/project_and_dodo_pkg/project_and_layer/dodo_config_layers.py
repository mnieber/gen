from titan.dodo_pkg.layer import LayerConfig


def get_for_project(project):
    return LayerConfig(
        dict(
            MENU=dict(
                session_id=project.kebab_name,
            ),
        )
    )
