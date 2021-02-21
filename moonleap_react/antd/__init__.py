from moonleap import add, extend, rule, tags
from moonleap.verbs import has
from moonleap_react.nodepackage import load_node_package_config
from moonleap_tools.tool import Tool

from . import css_imports


class Antd(Tool):
    pass


@tags(["antd"])
def create_antd(term, block):
    antd = Antd()
    add(antd, css_imports.get())
    add(antd, load_node_package_config(__file__))
    return antd


@rule("service", has, "antd")
def service_with_antd(service, antd):
    service.add_tool(antd)
    antd.output_paths.add_source(service)


@extend(Antd)
class ExtendAntd:
    pass
