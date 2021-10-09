from pathlib import Path

from moonleap import add, create, rule
from titan.react_pkg.module import create_module
from titan.react_pkg.nodepackage import load_node_package_config


@create("forms:module")
def create_forms_module(term, block):
    module = create_module(term, block)
    module.add_template_dir(Path(__file__).parent / "templates")
    add(module, load_node_package_config(__file__))
    return module


@rule("forms:module")
def forms_module_created(forms_module):
    forms_module.react_app.utils_module.use_packages(
        ["useScheduledCall", "ValuePicker", "slugify"]
    )
