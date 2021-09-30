from pathlib import Path

from moonleap import add, create
from titan.react_pkg.module import create_module
from titan.react_pkg.nodepackage import load_node_package_config


@create("forms:module")
def create_forms_module(term, block):
    module = create_module(term, block)
    module.add_template_dir(Path(__file__).parent / "templates")
    add(module, load_node_package_config(__file__))
    return module
