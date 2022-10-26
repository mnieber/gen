from pathlib import Path

from moonleap import create, kebab_to_camel, rule, u0
from moonleap.verbs import has
from titan.react_pkg.packages.use_react_packages import use_react_packages

from .resources import Picker

base_tags = {"picker": ["component"]}


@create("picker")
def create_picker(term):
    item_name = kebab_to_camel(term.data)
    name = f"{u0(item_name)}Picker"
    picker = Picker(item_name=item_name, name=name)
    picker.template_dir = Path(__file__).parent / "templates"
    return picker


@rule("module", has, "picker")
def create_utils_module(module, picker):
    use_react_packages(module.react_app.get_module("utils"), ["ValuePicker"])
