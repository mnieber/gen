from moonleap import MemFun, add, extend, render_templates, tags
from titan.react_pkg.nodepackage import load_node_package_config
from titan.project_pkg.service import Tool


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
