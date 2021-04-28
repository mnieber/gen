import moonleap.resource.props as P
from moonleap import MemFun, Prop, extend, render_templates, tags
from moonleap.verbs import has
from moonleap_react.component import Component
from moonleap_react.module import Module
from moonleap_react_module.api import Api

from . import props


class ConstantsApi(Api):
    pass


@tags(["constants:api"])
def create_constants_api(term, block):
    constants_api = ConstantsApi(name="api")
    return constants_api


@extend(ConstantsApi)
class ExtendConstantsApi:
    render = MemFun(render_templates(__file__))
    construct_item_list_section = MemFun(props.construct_item_list_section)
    import_api_section = Prop(props.import_api_section)


@extend(Module)
class ExtendModule:
    constants_api = P.child(has, "constants:api")
