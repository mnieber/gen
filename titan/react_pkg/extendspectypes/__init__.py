from moonleap import Prop, extend
from moonleap.typespec.field_spec import FieldSpec
from titan.api_pkg.item.resources import Item
from titan.api_pkg.itemlist.resources import ItemList
from titan.api_pkg.itemtype.resources import ItemType

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
    ts_form_type = Prop(props.item_type_ts_form_type)


@extend(FieldSpec)
class ExtendFieldSpec:
    ts_type = Prop(props.field_spec_ts_type)
    ts_default_value = Prop(props.field_spec_ts_default_value)
