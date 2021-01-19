import moonleap.resource.props as P
from leapproject.service import Service
from moonleap import MemFun, StoreOutputPaths, extend, render_templates, rule, tags
from moonleap.verbs import has

from . import props
from .resources import SetupFile, SetupFileConfig  # noqa


@tags(["setup-file"])
def create_setup_file(term, block):
    return SetupFile()


@rule("service", has, "setup-file")
def service_has_setup_file(service, setup_file):
    setup_file.output_paths.add_source(service)


class StoreSetupFileConfigs:
    setup_file_configs = P.tree("has", "setup-file-config")


@extend(SetupFile)
class ExtendSetupFile(StoreSetupFileConfigs, StoreOutputPaths):
    render = render_templates(__file__)
    service = P.parent(Service, has, "setup-file")
    get_setup_file_config = MemFun(props.get_setup_file_config)
