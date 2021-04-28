import moonleap.resource.props as P
from moonleap import MemFun, extend
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
    load_item_list_section = MemFun(props.load_item_list_section)
    save_list_item_section = MemFun(props.save_list_item_section)


@extend(Module)
class ExtendModule:
    apis = P.children(has, "api")
