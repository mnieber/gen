import moonleap.resource.props as P
from moonleap import MemFun, add, extend, kebab_to_camel, rule, tags
from moonleap.verbs import has, uses
from moonleap_react.nodepackage import load_node_package_config
from moonleap_react_module.flags import StoreFlags

from . import props
from .resources import AppModule  # noqa


@tags(["app:module"])
def create_app_module(term, block):
    module = AppModule(name=kebab_to_camel(term.data))
    module.add_template_dir(__file__, "templates")
    module.output_path = f"src/{module.name}"
    add(module, load_node_package_config(__file__))
    return module


@rule("service", has, "app:module")
def service_has_app_module(service, module):
    service.add_template_dir(__file__, "templates_service")


def meta():
    from moonleap_project.service import Service

    @extend(Service)
    class ExtendService:
        app_module = P.child(has, "app:module")

    @extend(AppModule)
    class ExtendAppModule(StoreFlags):
        get_flags = MemFun(props.get_flags)

    return [ExtendService, ExtendAppModule]
