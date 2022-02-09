from moonleap import Prop, extend
from titan.api_pkg.item.resources import Item
from titan.api_pkg.itemlist.resources import ItemList
from titan.api_pkg.itemtype.resources import ItemType
from titan.react_state_pkg.state.resources import State

from . import props


@extend(Item)
class ExtendItem:
    ts_type = Prop(props.item_ts_type)
    ts_var = Prop(props.item_ts_var)


@extend(ItemList)
class ExtendItemList:
    ts_type = Prop(props.item_list_ts_type)
    ts_var = Prop(props.item_list_ts_var)


@extend(ItemType)
class ExtendItemType:
    ts_type = Prop(props.item_type_ts_type)
    ts_type_import_path = Prop(props.item_type_ts_type_import_path)
    ts_form_type = Prop(props.item_type_ts_form_type)


@extend(State)
class ExtendState:
    ts_var = Prop(props.state_ts_var)
