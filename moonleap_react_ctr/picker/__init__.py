from moonleap import MemFun, Prop, add, extend, kebab_to_camel, render_templates, tags
from moonleap_react.nodepackage import load_node_package_config

from . import props
from .resources import Picker


@tags(["picker"])
def create_picker(term, block):
    name = kebab_to_camel(term.data)
    picker = Picker(item_name=name, name=f"{name}Picker")
    add(picker, load_node_package_config(__file__))
    return picker


@extend(Picker)
class ExtendPicker:
    render = MemFun(render_templates(__file__))
    item_type = Prop(props.item_type)
    create_router_configs = MemFun(props.create_router_configs)
