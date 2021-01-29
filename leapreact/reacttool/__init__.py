from leapreact.nodepackage import StoreNodePackageConfigs
from leaptools.tool import Tool
from moonleap import add, extend, render_templates, rule, tags


class ReactTool(Tool):
    pass


@extend(ReactTool)
class ExtendReactTool(StoreNodePackageConfigs):
    pass
