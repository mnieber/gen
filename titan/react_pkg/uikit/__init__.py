from moonleap import MemFun, RenderTemplates, add, extend, tags
from titan.project_pkg.service import Tool
from titan.react_pkg.nodepackage import load_node_package_config


class UIkit(Tool):
    pass


@tags(["uikit"])
def create_uikit(term, block):
    uikit = UIkit(name="uikit")
    uikit.output_path = "src"
    add(uikit, load_node_package_config(__file__))
    return uikit


@extend(UIkit)
class ExtendUIkit(RenderTemplates(__file__)):
    pass
