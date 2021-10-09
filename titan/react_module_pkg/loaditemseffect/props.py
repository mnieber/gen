from titan.react_view_pkg.pkg.create_component_router_config import (
    create_component_router_config,
)


def create_router_configs(self):
    return [create_component_router_config(self, url="")]


def _query(item_list):
    queries = item_list.provider_queries
    if queries:
        return queries[0]
    return None


def get_context(load_items_effect):
    _ = lambda: None
    _.query = _query(load_items_effect.item_list)

    class Sections:
        def import_query(self):
            if _.query:
                return f"import {{ {_.query.fun_name} }} from 'src/api/queries/{_.query.fun_name}"
            return ""

        def run_query(self):
            tab = " " * 8
            if _.query:
                return f"{tab}{_.query.fun_name}()"
            return ""

    return dict(sections=Sections())
