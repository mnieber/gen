from leaptools.tool import Tool
from moonleap import add, extend, rule, tags
from moonleap.verbs import has

from . import css_imports, node_package_configs


class Antd(Tool):
    pass


@tags(["antd"])
def create_antd(term, block):
    antd = Antd()
    add(antd, css_imports.get())
    add(antd, node_package_configs.get())
    return antd


@rule("service", has, "antd")
def service_with_antd(service, antd):
    service.add_tool(antd)
    antd.output_paths.add_source(service)


@extend(Antd)
class ExtendAntd:
    pass
