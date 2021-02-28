import moonleap.resource.props as P
from moonleap import MemFun, Prop, Rel, add, extend, rule, tags
from moonleap.verbs import has
from moonleap_project.service import Service
from moonleap_react.component import StoreCssImports
from moonleap_react.nodepackage import load_node_package_config
from moonleap_react_module.flags import StoreFlags

from . import props
from .resources import AppModule  # noqa


@tags(["app:module"])
def create_app_module(term, block):
    module = AppModule(name=term.data)
    module.add_template_dir(__file__, "templates")
    module.output_path = f"src/{module.name}"
    add(module, load_node_package_config(__file__))
    return module


@rule("service", has, "module")
def service_has_module(service, module):
    if module.name == "app":
        service.add_template_dir(__file__, "templates_service")
    else:
        return Rel(service.app_module.term, has, module.term)


@extend(Service)
class ExtendService:
    app_module = P.child(has, "app:module")


@extend(AppModule)
class ExtendAppModule(StoreCssImports, StoreFlags):
    css_import_lines = Prop(props.css_import_lines)
    get_flags = MemFun(props.get_flags)
    submodules = P.tree(has, "module")
