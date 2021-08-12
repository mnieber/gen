import moonleap.resource.props as P
from moonleap import add, add_source, extend, rule
from moonleap.verbs import configured_by, has
from titan.dodo_pkg.layer import StoreLayerConfigs
from titan.project_pkg.service import Service

from . import layer_configs


@rule("service")
def service_created(service):
    add(service, layer_configs.get_service_options(service))


@rule("service", configured_by, "layer")
def service_is_configured_in_layer(service, layer):
    add_source(
        [layer, "layer_configs"],
        service,
        "This layer receives layer configs from a service",
    )


@rule("service", has, "dockerfile")
def service_has_dockerfile(service, dockerfile):
    add(service, layer_configs.get_docker_options(service))


@rule("service", has, "tool")
def service_has_tool(service, tool):
    add_source(
        [service, "layer_configs"],
        tool,
        "This service receives layer configs from a tool",
    )


@extend(Service)
class ExtendService(
    StoreLayerConfigs,
):
    layer = P.child(configured_by, "layer")
