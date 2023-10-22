def get_helpers(_):
    class Helpers:
        project = _.vscode_project.project
        has_vandelay = bool([x for x in project.services if x.vandelay])

    return Helpers()


def get_meta_data_by_fn(_, __):
    return {
        "code-workspace.j2": {
            "name": f"{_.vscode_project.project.kebab_name}.code-workspace",
        }
    }
