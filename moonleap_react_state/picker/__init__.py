from moonleap import (
    MemFun,
    add,
    create_forward,
    extend,
    kebab_to_camel,
    render_templates,
    rule,
    tags,
    upper0,
)
from moonleap.verbs import has
from moonleap_react.nodepackage import load_node_package_config

from .resources import Picker


@tags(["picker"])
def create_picker(term, block):
    item_name = kebab_to_camel(term.data)
    name = f"{upper0(item_name)}Picker"
    picker = Picker(item_name=item_name, name=name)
    add(picker, load_node_package_config(__file__))
    return picker


@rule("module", has, "picker")
def create_utils_module(module, picker):
    module.service.utils_module.add_template_dir(__file__, "templates_utils")


@extend(Picker)
class ExtendPicker:
    render = MemFun(render_templates(__file__))
