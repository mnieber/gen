from dataclasses import dataclass

from moonleap import Resource, u0
from titan.react_pkg.pkg.ml_get import ml_react_app


@dataclass
class Component(Resource):
    name: str

    @property
    def react_tag(self):
        return f"<{u0(self.name)}/>"


def get_component_base_url(component, default_value):
    return ml_react_app(component).service.get_tweak_or(
        default_value, ["react_app", "components", component.name, "base_url"]
    )
