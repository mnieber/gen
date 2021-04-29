from dataclasses import dataclass

from moonleap import Resource
from moonleap_react.component import Component


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
            child_router_configs = child_component.create_router_configs()
            if not child_router_configs or len(child_router_configs) < 2:
                continue

            wrapper_router_configs = reduce_router_configs(child_router_configs[:-1])
            result = prepend_router_configs(wrapper_router_configs, result)

    return result


def prepend_router_configs(first, second):
    first_components = [x.component for x in first]
    second_filtered = [x for x in second if x.component not in first_components]
    return first + second_filtered
