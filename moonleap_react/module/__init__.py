import moonleap.resource.props as P
from moonleap import (
    Forward,
    Rel,
    StoreOutputPaths,
    extend,
    kebab_to_camel,
    rule,
    tags,
    word_to_term,
)
from moonleap.render.storetemplatedirs import StoreTemplateDirs
from moonleap.verbs import has
from moonleap_project.service import Service
from moonleap_react.nodepackage import StoreNodePackageConfigs

from .resources import Module  # noqa


@tags(["module"])
def create_module(term, block):
    module = Module(name=kebab_to_camel(term.data))
    module.output_path = f"src/{module.name}"
    return module


@rule("service", has, "module")
def service_has_module(service, module):
    module.output_paths.add_source(service)
    service.cra.node_package_configs.add_source(module)


def module_has_component_rel(module, component):
    return Forward(
        rel=Rel(module.term, has, word_to_term(":component")),
        subj_res=module,
        obj_res=component,
    )


@extend(Module)
class ExtendModule(StoreTemplateDirs, StoreNodePackageConfigs, StoreOutputPaths):
    service = P.parent(Service, has, "module")
