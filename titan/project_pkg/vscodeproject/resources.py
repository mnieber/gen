from dataclasses import dataclass

from moonleap import Resource, get_session


@dataclass
class VsCodeProject(Resource):
    @property
    def code_workspaces_dir(self):
        return get_session().settings.get("code_workspaces_dir")
