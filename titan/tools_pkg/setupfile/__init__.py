import moonleap.resource.props as P
from moonleap import Prop, RenderTemplates, extend, register_add, tags
from moonleap.verbs import has
from titan.project_pkg.service import Tool

from . import props
from .resources import SetupFile, SetupFileConfig  # noqa


@tags(["setup.cfg"])
def create_setup_file(term, block):
    return SetupFile(name="setup-file")


@register_add(SetupFileConfig)
def add_setup_file_config(resource, setup_file_config):
    resource.setup_file_configs.add(setup_file_config)


class StoreSetupFileConfigs:
    setup_file_configs = P.tree(has, "setup.cfg-config")


@extend(SetupFile)
class ExtendSetupFile(StoreSetupFileConfigs, RenderTemplates(__file__)):
    sections = Prop(props.Sections)


@extend(Tool)
class ExtendTool(StoreSetupFileConfigs):
    pass
