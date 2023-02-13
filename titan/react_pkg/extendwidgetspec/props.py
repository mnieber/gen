from moonleap import kebab_to_camel
from moonleap.blocks.term import match_term_to_pattern, str_to_term
from titan.react_view_pkg.widgetregistry import get_widget_reg


def widget_spec_handler_term_strs(widget_spec):
    return widget_spec.src_dict.setdefault("__handlers__", [])


def widget_spec_bvr_names(widget_spec):
    return [kebab_to_camel(x) for x in widget_spec.src_dict.setdefault("__bvrs__", [])]


def widget_spec_component(widget_spec):
    if not widget_spec.is_component:
        return None

    for component in get_widget_reg().components:
        if widget_term := str_to_term(widget_spec.widget_name):
            if match_term_to_pattern(component.meta.term, widget_term):
                return component

    raise Exception(f"Cannot find component for {widget_spec.widget_name}")


def widget_spec_get_bvr_names(widget_spec, recurse=False):
    ws = widget_spec
    while ws:
        if bvr_names := ws.bvr_names:
            return bvr_names
        ws = ws.parent if recurse else None
    return None
