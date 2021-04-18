from moonleap import MemFun, add, extend, render_templates, rule, tags
from moonleap.verbs import has
from moonleap_project.service import service_has_tool_rel
from moonleap_react.nodepackage import load_node_package_config
from moonleap_tools.tool import Tool


class Antd(Tool):
    pass


@tags(["antd"])
def create_antd(term, block):
    antd = Antd()
    antd.output_path = "src"
    add(antd, load_node_package_config(__file__))
    return antd


@rule("service", has, "antd")
def service_with_antd(service, antd):
    return service_has_tool_rel(service, antd)


@extend(Antd)
class ExtendAntd:
    render = MemFun(render_templates(__file__))
