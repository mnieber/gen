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


def get_component_base_url(component, default_value):
    return component.module.react_app.service.get_tweak_or(
        default_value, ["react_app", "components", component.name, "base_url"]
    )
