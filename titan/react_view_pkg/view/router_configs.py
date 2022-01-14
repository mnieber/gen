from moonleap.utils.case import l0
from titan.react_pkg.component.resources import get_component_base_url
from titan.react_view_pkg.router import RouterConfig


def _wraps(panel):
    return panel and bool(panel.typ.wraps_children)


def create_router_configs(self, named_component):
    base_url = get_component_base_url(self, l0(self.name))
    url = "/".join(([base_url] if base_url else []))
    router_config = RouterConfig(
        component=named_component,
        url=url,
        wraps=bool(self.wraps_children)
        or _wraps(self.top_panel)
        or _wraps(self.middle_panel)
        or _wraps(self.bottom_panel)
        or _wraps(self.left_panel)
        or _wraps(self.right_panel),
    )
    return [router_config]
