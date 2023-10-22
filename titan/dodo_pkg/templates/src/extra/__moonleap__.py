from moonleap.utils.case import sn


def get_meta_data_by_fn(_, __):
    return {
        "[project_dodo_commands]": {
            "name": f"{sn(_.project.name)}_commands",
        }
    }
