from leaptools.tool import Tool
from moonleap import MemFun, add, extend, render_templates, rule, tags
from moonleap.verbs import with_

from . import node_package_configs


class Prettier(Tool):
    pass


@tags(["prettier"])
def create_prettier(term, block):
    prettier = Prettier()
    add(prettier, node_package_configs.get())
    return prettier


@rule("create-react-app", with_, "prettier")
def cra_with_prettier(cra, prettier):
    cra.node_package_configs.add_source(prettier)
    prettier.output_paths.add_source(cra)


@extend(Prettier)
class ExtendPrettier:
    render = MemFun(render_templates(__file__, "templates/.prettierrc"))
