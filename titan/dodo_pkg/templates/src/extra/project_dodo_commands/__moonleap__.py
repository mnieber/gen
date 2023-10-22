from moonleap.utils.case import sn


def get_meta_data_by_fn(_, __):
    return {
        ".": {
            "name": f"{sn(_.project.name)}_dodo_commands",
        },
        "init-project.py.j2": {
            "name": f"init-{_.project.kebab_name}.py.j2",
        },
    }
