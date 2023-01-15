from moonleap import get_root_resource
from moonleap.blocks.term import match_term_to_pattern, word_to_term
from titan.react_view_pkg.pkg.build_widget_spec import build_widget_spec
from titan.react_view_pkg.widgetregistry import get_widget_reg


def build_component_widget_spec(component):
    component.build_output = build_widget_spec(component.widget_spec)
    get_root_resource().set_flags(component.build_output.flags)


def component_widget_spec(component):
    for widget_spec in get_widget_reg().widget_specs():
        if widget_spec.is_component_def:
            if widget_term := word_to_term(widget_spec.widget_name):
                if match_term_to_pattern(component.meta.term, widget_term):
                    return widget_spec
    return None
