from moonleap.blocks.term import match_term_to_pattern, word_to_term
from titan.react_view_pkg.widgetregistry import get_widget_reg


def widget_spec_handler_terms(widget_spec):
    return widget_spec.src_dict.setdefault("__handlers__", [])


def widget_spec_named_prop_terms(widget_spec):
    return widget_spec.src_dict.setdefault("__props__", [])


def widget_spec_named_default_prop_terms(widget_spec):
    return widget_spec.src_dict.setdefault("__default_props__", [])


def widget_spec_component(widget_spec):
    if not widget_spec.is_component:
        return None

    for component in get_widget_reg().components:
        if widget_term := word_to_term(widget_spec.widget_name):
            if match_term_to_pattern(component.meta.term, widget_term):
                return component

    raise Exception(f"Cannot find component for {widget_spec.widget_name}")


def component_widget_spec(component):
    for widget_spec in get_widget_reg().widget_specs():
        if widget_spec.is_component_def:
            if widget_term := word_to_term(widget_spec.widget_name):
                if match_term_to_pattern(component.meta.term, widget_term):
                    return widget_spec

    return None
