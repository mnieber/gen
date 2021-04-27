from moonleap import MemFun, add, extend, kebab_to_camel, render_templates, tags, upper0
from moonleap_react.nodepackage import load_node_package_config

from . import props
from .resources import Picker


@tags(["picker"])
def create_picker(term, block):
    item_name = kebab_to_camel(term.data)
    name = f"{upper0(item_name)}Picker"
    picker = Picker(item_name=item_name, name=name)
    add(picker, load_node_package_config(__file__))
    return picker


@extend(Picker)
class ExtendPicker:
    render = MemFun(render_templates(__file__))
    create_router_configs = MemFun(props.create_router_configs)
