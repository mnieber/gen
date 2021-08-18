from moonleap import RenderTemplates, add, extend, tags
from titan.project_pkg.service import Tool
from titan.react_pkg.nodepackage import load_node_package_config


class Prettier(Tool):
    pass


@tags(["prettier"])
def create_prettier(term, block):
    prettier = Prettier(name="prettier")
    add(prettier, load_node_package_config(__file__))
    return prettier


@extend(Prettier)
class ExtendPrettier(RenderTemplates(__file__)):
    pass
