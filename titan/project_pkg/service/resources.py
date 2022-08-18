import typing as T
from dataclasses import dataclass, field

from moonleap import RenderMixin, Resource, TemplateDirMixin, get_session


@dataclass
class Service(RenderMixin, Resource):
    name: str
    install_dir: str = "/app"
    env_files: T.List[str] = field(default_factory=lambda: [])
    env_files_dev: T.List[str] = field(default_factory=lambda: [])

    def get_tweak_or(self, default_value, rel_path):
        return get_session().get_tweak_or(
            default_value, ["services", self.name, *rel_path]
        )

    @property
    def pip(self):
        if getattr(self, "pip_compile", None):
            return "pip"
        return None

    @property
    def copy_source_to_prod_image(self):
        return get_session().get_tweak_or(
            True, ["services", self.name, "copy_source_to_prod_image"]
        )

    @property
    def ports(self):
        result = {}
        if getattr(self, "django_app", None):
            result["django_app"] = "8000"
        if getattr(self, "react_app", None):
            result["react_app"] = "3000"
        if getattr(self, "postgres", None):
            result["postgres"] = "5432"
        return result

    @property
    def serve_command_dev(self):
        if getattr(self, "django_app", None) or getattr(self, "react_app", None):
            return "make run-server"
        return None

    @property
    def shell(self):
        if getattr(self, "fish", None):
            return "fish"
        return "sh"


@dataclass
class Tool(TemplateDirMixin, RenderMixin, Resource):
    name: str
