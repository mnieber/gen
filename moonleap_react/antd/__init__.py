from moonleap import MemFun, add, extend, render_templates, tags
from moonleap_react.nodepackage import load_node_package_config
from moonleap_tools.tool import Tool


class Antd(Tool):
    pass


@tags(["antd"])
def create_antd(term, block):
    antd = Antd(name="antd")
    antd.output_path = "src"
    add(antd, load_node_package_config(__file__))
    return antd


@extend(Antd)
class ExtendAntd:
    render = MemFun(render_templates(__file__))
