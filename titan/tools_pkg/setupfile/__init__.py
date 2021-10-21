from pathlib import Path

import moonleap.resource.props as P
from moonleap import create, extend, register_add
from titan.project_pkg.service import Tool

from .props import get_context
from .resources import SetupFile, SetupFileConfig  # noqa

base_tags = [("setup.cfg", ["tool"])]


@create("setup.cfg")
def create_setup_file(term, block):
    setupFile = SetupFile(name="setup-file")
    setupFile.add_template_dir(Path(__file__).parent / "templates", get_context)
    return setupFile


@register_add(SetupFileConfig)
def add_setup_file_config(resource, setup_file_config):
    resource.setup_file_configs.add(setup_file_config)


class StoreSetupFileConfigs:
    setup_file_configs = P.tree("setup_file_configs")


@extend(SetupFile)
class ExtendSetupFile(StoreSetupFileConfigs):
    pass


@extend(Tool)
class ExtendTool(StoreSetupFileConfigs):
    pass
