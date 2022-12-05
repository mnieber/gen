import os

from moonleap.utils.fp import append_uniq


def add_div_open(builder):
    class_names = (
        [f'"{builder.widget_spec.widget_class_name}"']
        + builder.widget_spec.div_styles
        + (["props.className"] if builder.widget_spec.is_component_def else [])
    )

    for external_css_class in ("card",):
        if external_css_class in builder.widget_spec.div_styles:
            append_uniq(builder.output.external_css_classes, external_css_class)

    class_name = ", ".join(class_names)
    props_attr = os.linesep.join(builder.widget_spec.div_props)

    key = builder.widget_spec.div_key
    key_attr = f"key={{{key}}}" if key else ""
    builder.add_lines([f"<div {key_attr} className={{cn({class_name})}} {props_attr}>"])


def add_div_close(builder):
    builder.add_lines([f"</div>"])
