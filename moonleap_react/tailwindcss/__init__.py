from moonleap_tools.tool import Tool
from moonleap import MemFun, add, extend, render_templates, rule, tags
from moonleap.verbs import has

from . import node_package_configs


class TailwindCss(Tool):
    pass


@tags(["tailwind-css"])
def create_tailwind_css(term, block):
    tailwind_css = TailwindCss()
    add(tailwind_css, node_package_configs.get())
    return tailwind_css


@rule("service", has, "tailwind-css")
def service_has_tailwind_css(service, tailwind_css):
    service.add_tool(tailwind_css)
    tailwind_css.output_paths.add_source(service)


@extend(TailwindCss)
class ExtendTailwindCss:
    render = MemFun(render_templates(__file__))
