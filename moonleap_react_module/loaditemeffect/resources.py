import typing as T
from dataclasses import dataclass

from moonleap import upper0
from moonleap_react.component import Component


@dataclass
class LoadItemEffect(Component):
    item_name: str
    route_params: T.List[str]

    @property
    def name_postfix(self):
        return create_name_postfix(self.item_name, self.route_params)


def create_name_postfix(item_name, route_params):
    def _param_to_word(route_param):
        if route_param.startswith(item_name):
            route_param = route_param[len(item_name) :]
        return upper0(route_param)

    return "By" + "And".join([_param_to_word(x) for x in route_params])
