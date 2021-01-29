from leapreact.nodepackage import StoreNodePackageConfigs
from leaptools.tool import Tool
from moonleap import extend


class ReactTool(Tool):
    pass


@extend(ReactTool)
class ExtendReactTool(StoreNodePackageConfigs):
    pass
