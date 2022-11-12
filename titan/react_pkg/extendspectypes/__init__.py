from moonleap import Prop, extend
from titan.react_pkg.component import Component
from titan.types_pkg.item.resources import Item
from titan.types_pkg.itemlist.resources import ItemList
from titan.types_pkg.pkg.field_spec import FieldSpec
from titan.widgets_pkg.pkg.widget_spec import WidgetSpec

from . import props


@extend(Item)
class ExtendItem:
    ts_type = Prop(props.item_ts_type)
    ts_var = Prop(props.item_ts_var)
    ts_form_type = Prop(props.item_ts_form_type)


@extend(ItemList)
class ExtendItemList:
    ts_type = Prop(props.item_list_ts_type)
    ts_var = Prop(props.item_list_ts_var)


@extend(FieldSpec)
class ExtendFieldSpec:
    ts_type = Prop(props.field_spec_ts_type)
    ts_default_value = Prop(props.field_spec_ts_default_value)


@extend(WidgetSpec)
class ExtendWidgetSpec:
    component = Prop(props.widget_spec_component)


@extend(Component)
class ExtendComponent:
    widget_spec = Prop(props.component_widget_spec)
