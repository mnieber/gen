from moonleap import MemFun, add, extend, render_templates, tags
from titan.react_pkg.nodepackage import load_node_package_config
from titan.project_pkg.service import Tool


class Prettier(Tool):
    pass


@tags(["prettier"])
def create_prettier(term, block):
    prettier = Prettier(name="prettier")
    add(prettier, load_node_package_config(__file__))
    return prettier


@extend(Prettier)
class ExtendPrettier:
    render = MemFun(render_templates(__file__, "templates/.prettierrc"))
