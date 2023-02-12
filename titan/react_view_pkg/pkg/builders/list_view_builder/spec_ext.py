import ramda as R

from moonleap.utils.merge_into_config import merge_into_config
from titan.widgetspec.get_place_dict import get_place_dict


def spec_ext(list_view_builder, places, named_item_term_str, parent_widget_spec):
    extension = {}
    widget_spec = list_view_builder.widget_spec
    lvi_name = widget_spec.values.get("lvi-name") or _get_default_lvi_name(widget_spec)

    if "ListViewItem" not in places:
        extension.update(_lvi_spec(lvi_name))
    if "LviComponent" not in places:
        extension.update(
            _lvi_component_spec(
                widget_spec, lvi_name, named_item_term_str, parent_widget_spec
            )
        )
    return extension


def _lvi_spec(lvi_name):
    # This function returns a spec for the ListViewItem place. At this place,
    # we show a list view item component.
    return {
        f"ListViewItem with {lvi_name}": "pass",
    }


def _lvi_component_spec(widget_spec, lvi_name, named_item_term_str, parent_widget_spec):
    # This function returns a spec for the list view item component.
    lhs_contents = get_place_dict(widget_spec.src_dict, "LhsContents") or {
        "LhsContents with ItemFields": "display=1",
    }

    middle_slot = get_place_dict(widget_spec.src_dict, "MiddleSlot") or {}

    rhs_contents = get_place_dict(widget_spec.src_dict, "RhsContents") or {
        "RhsContents with LviButtons": "pass",
    }

    context_menu_value = parent_widget_spec.values.get("contextMenu")
    context_menu = f",contextMenu={context_menu_value}" if context_menu_value else ""

    body = {
        "__bvrs__": parent_widget_spec.bvr_names,
        "__dict__": {
            "item": named_item_term_str,
            "cnLhs": "__Title",
            "cnRhs": f"__Buttons{context_menu}",
        },
        **lhs_contents,
        **middle_slot,
        **rhs_contents,
    }

    # Mix in the body of the LviComponentMixin place, if any.
    merge_into_config(
        body,
        R.head(
            R.values(get_place_dict(widget_spec.src_dict, "LviComponentMixin") or {})
        )
        or {},
    )

    return {f"LviComponent with {lvi_name} as ListViewItem, Bar[p-2]": body}


def _get_default_lvi_name(widget_spec):
    default_lvi_name = widget_spec.root.widget_name
    if "-:" in default_lvi_name:
        default_lvi_name = default_lvi_name.replace("-:", "-") + "-item:view"
    else:
        pos = default_lvi_name.find(":")
        default_lvi_name = default_lvi_name[:pos] + "-item:view"
    return default_lvi_name
