from moonleap import extend, rule
from moonleap.verbs import has
from moonleap_project.service import Service
from moonleap_react_view.router.__init__ import StoreRouterConfigs


@rule("service", has, "tool")
def service_has_tool(service, tool):
    service.router_configs.add_source(tool)


@extend(Service)
class ExtendService(StoreRouterConfigs):
    pass
