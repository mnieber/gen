import ramda as R
from moonleap import get_tweaks
from moonleap_react.component.resources import get_component_base_url
from moonleap_react_view.router import RouterConfig
from moonleap_react_view.router.resources import reduce_router_configs


def _wraps(panel):
    return panel and panel.wraps_children


def _get_route_params(self):
    return R.path_or(
        [],
        ["services", self.module.service.name, "components", self.name, "route_params"],
    )(get_tweaks())


def create_router_configs(self):
    base_url = get_component_base_url(self, "")
    url = "/".join(
        ([base_url] if base_url else [])
        + [":" + x for x in _get_route_params(self) if x is not None]
    )
    router_config = RouterConfig(
        component=self,
        url=url,
        wraps=_wraps(self.top_panel)
        or _wraps(self.middle_panel)
        or _wraps(self.bottom_panel)
        or _wraps(self.left_panel)
        or _wraps(self.right_panel),
    )
    result = reduce_router_configs([router_config])
    return result
