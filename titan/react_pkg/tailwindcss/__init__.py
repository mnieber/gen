from pathlib import Path

from moonleap import Prop, add, create, extend
from titan.project_pkg.service import Tool
from titan.react_pkg.nodepackage import load_node_package_config
from titan.react_pkg.reactapp import ReactApp

from . import props


class TailwindCss(Tool):
    pass


base_tags = [("tailwind-css", ["tool"])]


@create("tailwind-css")
def create_tailwind_css(term, block):
    tailwind_css = TailwindCss(name="tailwind_css")
    tailwind_css.add_template_dir(Path(__file__).parent / "templates")
    add(tailwind_css, load_node_package_config(__file__))
    return tailwind_css


@extend(ReactApp)
class ExtendReactApp:
    has_tailwind_css = Prop(props.has_tailwind_css)
