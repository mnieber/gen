from moonleap_react_view.router.resources import prepend_router_configs


def create_router_configs(self):
    result = []

    state = self.module.state
    state_provider = state.state_provider if state else None
    if state_provider:
        result = prepend_router_configs(state_provider.create_router_configs(), result)

    return result
