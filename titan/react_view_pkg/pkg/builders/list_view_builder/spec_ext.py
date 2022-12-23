from widgetspec.get_place_dict import get_place_dict


def spec_ext(widget_spec, places):
    named_item_term_str = widget_spec.get_value_by_name("item")
    lvi_name = widget_spec.values.get("lvi-name") or _get_default_lvi_name(widget_spec)

    result = {}
    if "ListViewItem" not in places:
        result.update(_lvi_spec(lvi_name))
    if "LviComponent" not in places:
        result.update(_lvi_component_spec(widget_spec, lvi_name, named_item_term_str))
    return result


def _lvi_spec(lvi_name):
    return {
        f"ListViewItem with {lvi_name}": "pass",
    }


def _lvi_component_spec(widget_spec, lvi_name, named_item_term_str):
    lhs_contents = get_place_dict(widget_spec.src_dict, "LhsContents") or {
        "LhsContents with ItemFields": "display=1",
    }

    middle_slot = get_place_dict(widget_spec.src_dict, "MiddleSlot") or {}

    rhs_contents = get_place_dict(widget_spec.src_dict, "RhsContents") or {
        "RhsContents with LviButtons": "pass",
    }

    return {
        f"LviComponent with {lvi_name} as ListViewItem, Bar[p-2]": {
            "__default_props__": [named_item_term_str],
            "__attrs__": "cnLhs=__Title.cnRhs=__Buttons",
            **lhs_contents,
            **middle_slot,
            **rhs_contents,
        },
    }


def _get_default_lvi_name(widget_spec):
    default_lvi_name = widget_spec.root.widget_name
    if "-:" in default_lvi_name:
        default_lvi_name = default_lvi_name.replace("-:", "-") + "-item:view"
    else:
        pos = default_lvi_name.find(":")
        default_lvi_name = default_lvi_name[:pos] + "-item:view"
    return default_lvi_name
