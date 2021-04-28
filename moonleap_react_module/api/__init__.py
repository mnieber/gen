import moonleap.resource.props as P
from moonleap import MemFun, Prop, extend
from moonleap.verbs import has, provides
from moonleap_react.component import Component
from moonleap_react.module import Module

from . import props


class Api(Component):
    pass


@extend(Api)
class ExtendApi:
    item_lists = P.children(provides, "item-list")
    provides_item_list = MemFun(props.provides_item_list)
    construct_item_list_section = MemFun(props.construct_item_list_section)
    item_list_io_section = MemFun(props.item_list_io_section)
    import_api_section = Prop(props.import_api_section)


@extend(Module)
class ExtendModule:
    apis = P.children(has, "api")
