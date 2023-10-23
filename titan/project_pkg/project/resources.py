from dataclasses import dataclass

from moonleap import Resource, get_session


@dataclass
class Project(Resource):
    name: str
    kebab_name: str

    @property
    def opt_dir_fn(self):
        return get_session().get_setting_or(
            "/opt/projects/" + self.kebab_name, ["project", "opt_dir_fn"]
        )

    @property
    def has_python(self):
        return [service for service in self.services if service.is_python]
