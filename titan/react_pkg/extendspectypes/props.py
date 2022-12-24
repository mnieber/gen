from moonleap.blocks.term import match_term_to_pattern, word_to_term
from moonleap.utils.case import u0
from moonleap.utils.inflect import plural
from titan.react_view_pkg.widgetregistry import get_widget_reg


def ts_type_from_type_name(x):
    return f"{u0(x)}T"


def item_ts_type(item):
    return ts_type_from_type_name(item.type_name)


def item_ts_var(item):
    return item.item_name


def item_list_ts_type(item_list):
    return f"{ts_type_from_type_name(item_list.item.type_name)}[]"


def item_list_ts_var(item_list):
    return plural(item_list.item_name)


def field_spec_ts_type(field_spec):
    if field_spec.field_type in ("fk", "form") and field_spec.target:
        return f"{field_spec.target}T"

    if field_spec.field_type in ("relatedSet",) and field_spec.target:
        return f"{field_spec.target}T[]"

    if field_spec.choices:
        return " | ".join([f"'{label}'" for choice, label in field_spec.choices])

    if field_spec.field_type in (
        "string",
        "text",
        "json",
        "url",
        "slug",
        "uuid",
        "image",
        "markdown",
    ):
        return "string"

    if field_spec.field_type in ("string[]", "uuid[]"):
        return "string[]"

    if field_spec.field_type in ("int[]",):
        return "int[]"

    if field_spec.field_type in ("boolean",):
        return "boolean"

    if field_spec.field_type in ("int", "float"):
        return "number"

    if field_spec.field_type in ("date",):
        return "Date"

    raise Exception(f"Cannot deduce graphql type for {field_spec.field_type}")


def field_spec_ts_default_value(field_spec):
    if field_spec.field_type in ("string", "text", "json", "url", "slug"):
        return "''"

    if field_spec.field_type in ("boolean",):
        return "false"

    if field_spec.field_type in ("int", "float"):
        return "0"

    raise Exception(f"Cannot deduce ts default value for {field_spec.field_type}")


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
