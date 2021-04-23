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


def meta():
    from moonleap_project.service import Service

    @extend(Module)
    class ExtendModule(StoreTemplateDirs, StoreNodePackageConfigs, StoreOutputPaths):
        service = P.parent(Service, has, "module")

    @extend(Service)
    class ExtendService:
        modules = P.children(has, "module")

    return [ExtendModule, ExtendService]
