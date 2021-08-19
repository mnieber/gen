from moonleap import RenderTemplates, extend, kebab_to_camel, rule, tags, upper0
from moonleap.verbs import has

from .resources import Picker


@tags(["picker"])
def create_picker(term, block):
    item_name = kebab_to_camel(term.data)
    name = f"{upper0(item_name)}Picker"
    picker = Picker(item_name=item_name, name=name)
    return picker


@rule("module", has, "picker")
def create_utils_module(module, picker):
    module.react_app.utils_module.use_packages(["ValuePicker"])


@extend(Picker)
class ExtendPicker(RenderTemplates(__file__)):
    pass
