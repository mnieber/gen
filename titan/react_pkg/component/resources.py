from dataclasses import dataclass

import ramda as R
from moonleap import Resource, get_session, upper0


@dataclass
class Component(Resource):
    name: str

    @property
    def react_tag(self):
        return f"<{upper0(self.name)}/>"


def get_component_base_url(component, default_value):
    component_settings = R.path_or(
        {},
        [
            "services",
            component.module.react_app.service.name,
            "react_app",
            "components",
            component.name,
        ],
    )(get_session().get_tweaks())

    return component_settings.get("base_url", default_value)
