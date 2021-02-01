from leaptools.tool import Tool
from moonleap import MemFun, add, extend, render_templates, rule, tags
from moonleap.verbs import uses

from . import node_package_configs


class CreateReactApp(Tool):
    pass


@tags(["create-react-app"])
def create_cra(term, block):
    cra = CreateReactApp()
    add(cra, node_package_configs.get())
    return cra


@rule("node-package", uses, "create-react-app")
def node_package_uses_cra(node_package, cra):
    node_package.service.add_tool(cra)


@extend(CreateReactApp)
class ExtendCreateReactApp:
    render = MemFun(render_templates(__file__))
