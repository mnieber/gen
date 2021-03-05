from moonleap import MemFun, add, extend, render_templates, rule, tags
from moonleap.verbs import has
from moonleap_project.service import service_has_tool_rel
from moonleap_react.nodepackage import load_node_package_config
from moonleap_tools.tool import Tool


class Prettier(Tool):
    pass


@tags(["prettier"])
def create_prettier(term, block):
    prettier = Prettier()
    add(prettier, load_node_package_config(__file__))
    return prettier


@rule("service", has, "prettier")
def service_has_prettier(service, prettier):
    prettier.output_paths.add_source(service)
    return service_has_tool_rel(service, prettier)


@extend(Prettier)
class ExtendPrettier:
    render = MemFun(render_templates(__file__, "templates/.prettierrc"))
