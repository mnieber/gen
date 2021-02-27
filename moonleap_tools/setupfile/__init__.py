import moonleap.resource.props as P
from moonleap import (
    MemFun,
    StoreOutputPaths,
    extend,
    register_add,
    render_templates,
    rule,
    tags,
)
from moonleap.verbs import has
from moonleap_project.service import Service

from . import props
from .resources import SetupFile, SetupFileConfig  # noqa


@tags(["setup.cfg"])
def create_setup_file(term, block):
    return SetupFile()


@rule("service", has, "setup.cfg")
def service_has_setup_file(service, setup_file):
    setup_file.output_paths.add_source(service)


@register_add(SetupFileConfig)
def add_setup_file_config(resource, setup_file_config):
    resource.setup_file_configs.add(setup_file_config)


class StoreSetupFileConfigs:
    setup_file_configs = P.tree("has", "setup.cfg-config")


@extend(SetupFile)
class ExtendSetupFile(StoreSetupFileConfigs, StoreOutputPaths):
    render = MemFun(render_templates(__file__))
    service = P.parent(Service, has, "setup.cfg")
    get_setup_file_config = MemFun(props.get_setup_file_config)
