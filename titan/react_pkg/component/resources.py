from dataclasses import dataclass

from moonleap import RenderMixin, Resource, TemplateDirMixin, u0


@dataclass
class Component(TemplateDirMixin, RenderMixin, Resource):
    name: str

    @property
    def react_tag(self):
        return f"<{u0(self.name)}/>"

    def get_title(self):
        return self.name
