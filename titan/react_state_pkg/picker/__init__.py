from pathlib import Path

from moonleap import create, kebab_to_camel, rule, u0
from moonleap.verbs import has
from titan.react_pkg.pkg.ml_get import ml_react_app

from .resources import Picker

base_tags = [("picker", ["component"])]


@create("picker")
def create_picker(term):
    item_name = kebab_to_camel(term.data)
    name = f"{u0(item_name)}Picker"
    picker = Picker(item_name=item_name, name=name)
    picker.add_template_dir(Path(__file__).parent / "templates")
    return picker


@rule("module", has, "picker")
def create_utils_module(module, picker):
    ml_react_app(module).utils_module.use_packages(["ValuePicker"])
