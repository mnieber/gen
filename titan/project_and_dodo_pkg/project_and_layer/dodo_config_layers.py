from titan.dodo_pkg.layer import LayerConfig


def get(project):
    return LayerConfig(
        dict(
            MENU=dict(
                session_id=project.name_snake,
            ),
        )
    )
