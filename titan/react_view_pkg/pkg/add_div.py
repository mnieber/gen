import os

from moonleap.utils.fp import append_uniq


def add_div_open(builder, div_attrs=None):
    div_attrs = div_attrs or {}
    class_names = (
        [f'"{builder.output.widget_class_name}"']
        + div_attrs.get("classes", [])
        + builder.widget_spec.styles
        + (["props.className"] if builder.widget_spec.is_component_def else [])
    )

    for external_css_class in ("card",):
        if external_css_class in div_attrs.get("classes", []):
            append_uniq(builder.output.external_css_classes, external_css_class)

    class_name = ", ".join(class_names)
    handlers_attr = os.linesep.join(div_attrs.get("handlers", []))

    key = div_attrs.get("key")
    key_attr = f"key={{{key}}}" if key else ""
    builder.add_lines(
        [f"<div {key_attr} className={{cn({class_name})}} {handlers_attr}>"]
    )


def add_div_close(builder):
    builder.add_lines([f"</div>"])
