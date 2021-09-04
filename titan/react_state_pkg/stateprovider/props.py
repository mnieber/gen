from moonleap.utils.case import lower0
from moonleap.utils.inflect import plural
from titan.react_pkg.component.resources import get_component_base_url
from titan.react_pkg.router_and_module.props import create_component_router_config


def create_router_configs(self):
    result = []

    if self.state:
        router_config = create_component_router_config(
            self, wraps=True, url=get_component_base_url(self, "")
        )
        result.append(router_config)

    return result


class Sections:
    def __init__(self, res):
        self.res = res

    def default_props(self):
        result = ""

        if self.res.state:
            result = f"      {self.res.state.name}State: () => state,\n"
            store_by_item_name = self.res.state.store_by_item_name
            for item_name, bvrs in self.res.state.bvrs_by_item_name.items():
                store = store_by_item_name.get(item_name)
                items_name = plural(item_name)

                result += (
                    f"      {items_name}: () => state.outputs.{items_name}Display,\n"
                )
                result += f"      {items_name}ResUrl: () => {lower0(store.name)}.resUrls().{item_name}ById,\n"  # noqa: E501

                for bvr in bvrs:
                    result += bvr.sections.default_props(store)
        return result
