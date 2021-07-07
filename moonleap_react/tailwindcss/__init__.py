from moonleap import MemFun, add, extend, render_templates, tags
from moonleap_react.nodepackage import load_node_package_config
from moonleap_tools.tool import Tool


class TailwindCss(Tool):
    pass


@tags(["tailwind-css"])
def create_tailwind_css(term, block):
    tailwind_css = TailwindCss(name="tailwind")
    add(tailwind_css, load_node_package_config(__file__))
    return tailwind_css


@extend(TailwindCss)
class ExtendTailwindCss:
    render = MemFun(render_templates(__file__))
