from leaptools.tool import Tool
from moonleap import add, extend, render_templates, rule, tags
from moonleap.verbs import with_

from . import node_package_configs


class TailwindCss(Tool):
    pass


@tags(["tailwind-css"])
def create_tailwind_css(term, block):
    tailwind_css = TailwindCss()
    add(tailwind_css, node_package_configs.get())
    return tailwind_css


@rule("create-react-app", with_, "tailwind-css")
def cra_with_tailwind_css(cra, tailwind_css):
    cra.node_package_configs.add_source(tailwind_css)
    tailwind_css.output_paths.add_source(cra)


@extend(TailwindCss)
class ExtendTailwindCss:
    render = render_templates(__file__)
