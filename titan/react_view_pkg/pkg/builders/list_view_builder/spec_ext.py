def spec_ext(widget_spec, places):
    named_item_term_str = widget_spec.get_value_by_name("item")
    lvi_name = widget_spec.get_value_by_name("lvi-name") or _get_default_lvi_name(
        widget_spec
    )

    result = {}
    if "ListViewItem" not in places:
        result.update(_lvi_spec(lvi_name))
    if "LviComponent" not in places:
        result.update(_lvi_component_spec(lvi_name, named_item_term_str))
    return result


def _lvi_spec(lvi_name):
    return {
        f"ListViewItem with {lvi_name}": "pass",
    }


def _lvi_component_spec(lvi_name, named_item_term_str):
    return {
        f"LviComponent with {lvi_name} as ListViewItem, Bar[p-2]": {
            "__default_props__": [named_item_term_str],
            "LhsSlot with RowSkewer[justify=start.cn=__Fields]": {
                "ItemFields": "display=1"
            },
            "RhsSlot with RowSkewer[justify=end.cn=__Buttons]": {"LviButtons": "pass"},
        },
    }


def _lvi_component_spec_2(lvi_name, named_item_term_str):
    return {
        f"LviComponent with {lvi_name} as ListViewItem, Bar[p-2]": {
            "__default_props__": [named_item_term_str],
            "LhsContents[cn=__Fields] with ItemFields": "display=1",
            "RhsContents[cn=__Buttons] with LviButtons": "pass",
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
