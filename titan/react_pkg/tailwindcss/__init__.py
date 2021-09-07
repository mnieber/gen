from pathlib import Path

from moonleap import add, create
from titan.project_pkg.service import Tool
from titan.react_pkg.nodepackage import load_node_package_config


class TailwindCss(Tool):
    pass


@create("tailwind-css", ["tool"])
def create_tailwind_css(term, block):
    tailwind_css = TailwindCss(name="tailwind")
    tailwind_css.add_template_dir(Path(__file__).parent / "templates")
    add(tailwind_css, load_node_package_config(__file__))
    return tailwind_css
