from titan.dodo_pkg.layer import LayerConfig


def get_for_menu(project):
    return LayerConfig(
        dict(
            MENU=dict(
                session_id=project.kebab_name,
            ),
        )
    )
