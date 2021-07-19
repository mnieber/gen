from moonleap import MemFun, add, extend, render_templates, tags
from moonleap_react.nodepackage import load_node_package_config
from moonleap_tools.tool import Tool


class UIkit(Tool):
    pass


@tags(["uikit"])
def create_uikit(term, block):
    uikit = UIkit(name="uikit")
    uikit.output_path = "src"
    add(uikit, load_node_package_config(__file__))
    return uikit


@extend(UIkit)
class ExtendUIkit:
    render = MemFun(render_templates(__file__))
