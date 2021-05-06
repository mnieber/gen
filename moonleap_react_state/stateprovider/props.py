from moonleap.utils.inflect import plural
from moonleap_react_view.router.resources import prepend_router_configs
from moonleap_react_view.router_and_module.props import create_component_router_config


def create_router_configs(self):
    router_configs = create_component_router_config(
        self, wraps=True, url=self.state.name
    )
    result = [router_configs]

    store = self.module.store
    load_items_effects = (store.module.load_items_effects) if store else None
    for load_items_effect in load_items_effects or []:
        result = prepend_router_configs(
            result, load_items_effect.create_router_configs()
        )

    return result


def default_props_section(self):
    result = f"      {self.state.name}State: () => state,\n"
    store_by_item_name = self.state.store_by_item_name
    for item_name, bvrs in self.state.bvrs_by_item_name.items():
        item_names = plural(item_name)

        result += f"      {item_names}: () => state.outputs.{item_names}Display,\n"

        store = store_by_item_name.get(item_name)
        for bvr in bvrs:
            result += bvr.default_props_section(store)
    return result
