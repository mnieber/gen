from pathlib import Path

from moonleap import add, create
from titan.project_pkg.service import Tool
from titan.react_pkg.nodepackage import load_node_package_config


class Prettier(Tool):
    pass


base_tags = [("prettier", ["tool"])]


@create("prettier")
def create_prettier(term, block):
    prettier = Prettier(name="prettier")
    prettier.add_template_dir(Path(__file__).parent / "templates")
    add(prettier, load_node_package_config(__file__))
    return prettier
