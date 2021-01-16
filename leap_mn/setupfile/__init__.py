import moonleap.resource.props as P
from moonleap import StoreOutputPaths, extend, render_templates, tags

from . import props
from .resources import SetupFile, SetupFileConfig  # noqa


@tags(["setup-file"])
def create_setup_file(term, block):
    return SetupFile()


class StoreSetupFileConfigs:
    setup_file_configs = P.tree(
        "has", "setup-file-config", merge=props.merge, initial=SetupFileConfig({})
    )


@extend(SetupFile)
class ExtendSetup_file(StoreSetupFileConfigs, StoreOutputPaths):
    render = render_templates(__file__)
