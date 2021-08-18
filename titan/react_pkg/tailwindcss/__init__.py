from moonleap import RenderTemplates, add, extend, tags
from titan.project_pkg.service import Tool
from titan.react_pkg.nodepackage import load_node_package_config


class TailwindCss(Tool):
    pass


@tags(["tailwind-css"])
def create_tailwind_css(term, block):
    tailwind_css = TailwindCss(name="tailwind")
    add(tailwind_css, load_node_package_config(__file__))
    return tailwind_css


@extend(TailwindCss)
class ExtendTailwindCss(RenderTemplates(__file__)):
    pass
