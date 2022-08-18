def get_helpers(_):
    class Helpers:
        project = _.vscode_project.project
        has_vandelay = bool([x for x in project.services if x.vandelay])

    return Helpers()
