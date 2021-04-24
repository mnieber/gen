from moonleap import MemFun, add, extend, render_templates, tags
from moonleap_react.nodepackage import load_node_package_config
from moonleap_tools.tool import Tool


class Prettier(Tool):
    pass


@tags(["prettier"])
def create_prettier(term, block):
    prettier = Prettier()
    add(prettier, load_node_package_config(__file__))
    return prettier


@extend(Prettier)
class ExtendPrettier:
    render = MemFun(render_templates(__file__, "templates/.prettierrc"))
