from moonleap_dodo.layer import LayerConfig


def get(project):
    return LayerConfig(
        dict(
            MENU=dict(
                session_id=project.name_snake,
            ),
        )
    )
