from moonleap import create_forward, get_root_resource
from moonleap.blocks.term import match_term_to_pattern, word_to_term
from moonleap.blocks.verbs import has
from titan.react_view_pkg.pkg.build_widget_spec import build_widget_spec
from titan.react_view_pkg.pkg.preprocess_widget_spec import preprocess_widget_spec
from titan.react_view_pkg.widgetregistry import get_widget_reg


def build_component_widget_spec(component):
    widget_specs_memo = list(get_widget_reg().widget_specs())

    preprocess_widget_spec(component.widget_spec)
    component.build_output = build_widget_spec(component.widget_spec)
    get_root_resource().set_flags(component.build_output.flags)

    forwards = []
    new_widget_specs = [
        x for x in get_widget_reg().widget_specs() if x not in widget_specs_memo
    ]
    for widget_spec in new_widget_specs:
        forwards += create_forwards_for_widget_spec(
            component.module.react_app, widget_spec
        )
    return forwards


def component_widget_spec(component):
    for widget_spec in get_widget_reg().widget_specs():
        if widget_spec.is_component_def:
            if widget_term := word_to_term(widget_spec.widget_name):
                if match_term_to_pattern(component.meta.term, widget_term):
                    return widget_spec
    return None


def create_forwards_for_widget_spec(react_app, widget_spec):
    react_module_term_str = f"{widget_spec.module_name}:module"
    component_term_str = widget_spec.widget_name
    return [
        create_forward(react_app, has, react_module_term_str),
        create_forward(react_module_term_str, has, component_term_str),
    ]
