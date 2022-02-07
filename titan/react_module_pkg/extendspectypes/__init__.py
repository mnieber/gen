from moonleap import Prop, extend
from titan.api_pkg.item.resources import Item
from titan.api_pkg.itemlist.resources import ItemList
from titan.api_pkg.itemtype.resources import ItemType

from . import props


@extend(Item)
class ExtendItem:
    ts_type = Prop(props.item_ts_type)


@extend(ItemList)
class ExtendItemList:
    ts_type = Prop(props.item_list_ts_type)


@extend(ItemType)
class ExtendItemType:
    ts_type = Prop(props.item_type_ts_type)
    ts_type_import_path = Prop(props.item_type_ts_type_import_path)
