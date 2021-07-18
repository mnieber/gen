import ramda as R
from moonleap import get_tweaks
from moonleap_react_view.router import RouterConfig
from moonleap_react_view.router.resources import reduce_router_configs


def create_router_configs(self):
    router_configs = reduce_router_configs([RouterConfig(component=self, url="")])
    return router_configs


def collapses(self):
    return R.path_or(
        True,
        ["services", self.module.service.name, "components", self.name, "collapses"],
    )(get_tweaks())


def root_component(self):
    wraps = self.shows_children
    if len(self.child_components) == 0 and not wraps:
        return None

    collapses = self.collapses
    return (
        self.child_components[0]
        if len(self.child_components) == 1 and collapses
        else self
    )
