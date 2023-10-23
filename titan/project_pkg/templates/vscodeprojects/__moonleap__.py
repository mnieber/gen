def get_helpers(_):
    class Helpers:
        has_vandelay = bool([x for x in _.project.services if x.vandelay])

    return Helpers()


def get_meta_data_by_fn(_, __):
    return {
        "code-workspace.j2": {
            "name": f"{_.project.kebab_name}.code-workspace",
        }
    }
