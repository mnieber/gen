from moonleap import MemFun, add, extend, render_templates, rule, tags
from moonleap.verbs import has
from moonleap_project.service import service_has_tool_rel
from moonleap_react.nodepackage import load_node_package_config
from moonleap_tools.tool import Tool


class TailwindCss(Tool):
    pass


@tags(["tailwind-css"])
def create_tailwind_css(term, block):
    tailwind_css = TailwindCss()
    add(tailwind_css, load_node_package_config(__file__))
    return tailwind_css


@rule("service", has, "tailwind-css")
def service_has_tailwind_css(service, tailwind_css):
    return service_has_tool_rel(service, tailwind_css)


@extend(TailwindCss)
class ExtendTailwindCss:
    render = MemFun(render_templates(__file__))
