import typing as T
from dataclasses import dataclass, field

from moonleap import Resource
from titan.react_pkg.component import Component


class Router(Component):
    pass


@dataclass
class RouterConfig(Resource):
    component: Component
    url: str
    params: T.List[str] = field(default_factory=list)
    wraps: bool = False
    side_effects: T.List[T.Any] = field(default_factory=list)


def reduce_router_configs(router_configs, base_route):
    result = []

    for router_config in router_configs:
        child_components = getattr(router_config.component.typ, "child_components", [])
        for child_component in child_components:
            # The last router config always corresponds to the child component itself.
            # Any preceeding router configs supply dependencies
            # (e.g. state providers, load effects, etc)
            supporting_router_configs = child_component.typ.create_router_configs(
                named_component=child_component
            )[:-1]
            if not supporting_router_configs:
                continue

            preceeding_router_configs = reduce_router_configs(supporting_router_configs)
            result = concat_router_configs(preceeding_router_configs, result)

    result.extend(router_configs)
    return result


def concat_router_configs(first, second):
    first_components = [x.component for x in first]
    second_filtered = [x for x in second if x.component not in first_components]
    return first + second_filtered
