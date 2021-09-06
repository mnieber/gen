from dataclasses import dataclass

from moonleap import Resource, upper0


@dataclass
class Component(Resource):
    name: str

    @property
    def react_tag(self):
        return f"<{upper0(self.name)}/>"


def get_component_base_url(component, default_value):
    return component.module.react_app.service.get_tweak_or(
        default_value, ["react_app", "components", component.name, "base_url"]
    )
