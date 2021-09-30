from pathlib import Path

from moonleap import add, create
from titan.project_pkg.service import Tool
from titan.react_pkg.nodepackage import load_node_package_config


class UIkit(Tool):
    pass


base_tags = [("uikit", ["tool"])]


@create("uikit")
def create_uikit(term, block):
    uikit = UIkit(name="uikit")
    uikit.add_template_dir(Path(__file__).parent / "templates")
    uikit.output_path = "src"
    add(uikit, load_node_package_config(__file__))
    return uikit
