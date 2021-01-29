from leapreact.reacttool import ReactTool
from moonleap import add, rule, tags
from moonleap.verbs import with_

from . import node_package_configs


class TailwindCss(ReactTool):
    pass


@tags(["tailwind-css"])
def create_tailwind_css(term, block):
    tailwind_css = TailwindCss()
    add(tailwind_css, node_package_configs.get())
    return tailwind_css


@rule("create-react-app", with_, "tailwind-css")
def cra_with_tailwind_css(cra, tailwind_css):
    cra.node_package_configs.add_source(tailwind_css)
