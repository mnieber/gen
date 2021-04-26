from moonleap.utils.inflect import plural
from moonleap_react_view.router.resources import prepend_router_configs
from moonleap_react_view.router_and_module.props import create_component_router_config


def create_router_configs(self):
    router_configs = create_component_router_config(
        self, wraps=True, url=plural(self.item_name)
    )
    result = [router_configs]

    store = self.module.store
    load_items_effect = store.load_items_effect if store else None
    if load_items_effect:
        result = prepend_router_configs(
            result, load_items_effect.create_router_configs()
        )

    return result