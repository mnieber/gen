import moonleap.resource.props as P
from moonleap import MemFun, Prop, extend, register_add, render_templates, tags
from moonleap.verbs import has
from moonleap_project.service import Tool

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


def meta():
    from moonleap_project.service import Service

    @extend(SetupFile)
    class ExtendSetupFile(StoreSetupFileConfigs):
        render = MemFun(render_templates(__file__))
        service = P.parent(Service, has)
        p_section_setup_file_config = Prop(props.p_section_setup_file_config)

    @extend(Tool)
    class ExtendTool(StoreSetupFileConfigs):
        pass

    return [ExtendSetupFile, ExtendTool]
