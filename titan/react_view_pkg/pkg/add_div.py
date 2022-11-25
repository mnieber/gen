import os

from moonleap.utils.fp import append_uniq


def add_div_open(builder, classes=None, handlers=None):
    class_names = (
        [f'"{builder.output.widget_class_name}"']
        + (classes or [])
        + (builder.widget_spec.styles)
        + (["props.className"] if builder.widget_spec.is_component_def else [])
    )

    for external_css_class in ("card",):
        if external_css_class in (classes or []):
            append_uniq(builder.output.external_css_classes, external_css_class)

    class_name = ", ".join(class_names)
    handlers_attr = os.linesep.join(handlers or [])
    builder.add_lines([f"<div className={{cn({class_name})}} {handlers_attr}>"])


def add_div_close(builder):
    builder.add_lines([f"</div>"])
