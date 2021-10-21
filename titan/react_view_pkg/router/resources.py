from dataclasses import dataclass

from moonleap import Resource
from titan.react_pkg.component import Component


class Router(Component):
    pass


@dataclass
class RouterConfig(Resource):
    component: Component
    url: str
    wraps: bool = False


def reduce_router_configs(router_configs):
    result = list(router_configs)

    for router_config in router_configs:
        for child_component in router_config.component.child_components:
            # The last router config always corresponds to the child component itself.
            # Any preceeding router configs supply dependencies
            # (e.g. state providers, load effects, etc)
            supporting_router_configs = child_component.typ.create_router_configs()[:-1]
            if not supporting_router_configs:
                continue

            preceeding_router_configs = reduce_router_configs(supporting_router_configs)
            result = concat_router_configs(preceeding_router_configs, result)

    return result


def concat_router_configs(first, second):
    first_components = [x.component for x in first]
    second_filtered = [x for x in second if x.component not in first_components]
    return first + second_filtered
