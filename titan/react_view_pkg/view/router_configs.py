from titan.react_pkg.component.resources import get_component_base_url
from titan.react_pkg.pkg.ml_get import ml_react_app
from titan.react_view_pkg.router import RouterConfig
from titan.react_view_pkg.router.resources import reduce_router_configs


def _wraps(panel):
    return panel and bool(panel.wrapped_components)


def _get_route_params(self):
    return ml_react_app(self).service.get_tweak_or(
        [],
        [
            "react_app",
            "components",
            self.name,
            "route_params",
        ],
    )


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
