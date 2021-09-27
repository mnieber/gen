import typing as T
from dataclasses import dataclass

from moonleap import upper0
from moonleap.utils.case import lower0
from titan.react_pkg.component import Component


@dataclass
class LoadItemEffect(Component):
    route_params: T.Optional[T.List[str]] = None
    item_name: T.Optional[str] = None

    @property
    def name_postfix(self):
        return create_name_postfix(self.name, self.route_params)


def shorten_route_params(route_params, item_name):
    def _param_to_word(route_param):
        if route_param.startswith(item_name):
            cutoff_index = len(item_name)
            route_param = lower0(route_param[cutoff_index:])
        return route_param

    return [_param_to_word(x) for x in route_params]


def create_name_postfix(item_name, route_params):
    return "and-".join(shorten_route_params(route_params, item_name))
