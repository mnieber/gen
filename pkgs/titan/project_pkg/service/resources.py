from dataclasses import dataclass

from moonleap import RenderMixin, Resource, TemplateDirMixin, get_session


@dataclass
class Service(RenderMixin, Resource):
    name: str
    install_dir: str = "/app"

    def get_setting_or(self, default_value, rel_path):
        return get_session().get_setting_or(
            default_value, ["services", self.name, *rel_path]
        )

    @property
    def pip(self):
        if getattr(self, "pip_compile", None):
            return "pip"
        return None

    @property
    def copy_source_to_prod_image(self):
        return self.get_setting_or(True, ["copy_source_to_prod_image"])

    @property
    def has_django_app(self):
        return getattr(self, "django_app", None)

    @property
    def has_react_app(self):
        return getattr(self, "react_app", None)

    @property
    def has_postgres(self):
        return self.docker_image and self.docker_image.name.startswith("postgres")

    @property
    def ports(self):
        result = {}
        if self.has_django_app:
            result["django_app"] = "8000"
        if self.has_react_app:
            result["react_app"] = "3000"
        if self.has_postgres:
            result["postgres"] = "5432"
        return result

    @property
    def has_env(self):
        if self.has_django_app:
            return True
        if self.has_react_app:
            return True
        if self.has_postgres:
            return True
        return False

    @property
    def serve_command_dev(self):
        if self.has_django_app or self.has_react_app:
            return "make run-server"
        return None

    @property
    def shell(self):
        if getattr(self, "fish", None):
            return "fish"
        return "sh"

    @property
    def npm_source_maps(self):
        return self.get_setting_or({}, ["npm_source_maps"])

    @property
    def pypi_source_maps(self):
        return self.get_setting_or({}, ["pypi_source_maps"])


@dataclass
class Tool(TemplateDirMixin, RenderMixin, Resource):
    name: str
