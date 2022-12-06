import os


def add_div_open(builder):
    class_names = (
        [f'"{builder.widget_spec.widget_class_name}"']
        + builder.widget_spec.div_styles
        + (["props.className"] if builder.widget_spec.is_component_def else [])
    )

    class_name = ", ".join(class_names)
    props_attr = os.linesep.join(builder.widget_spec.div_attrs)

    key = builder.widget_spec.div_key
    key_attr = f"key={{{key}}}" if key else ""
    builder.add_lines([f"<div {key_attr} className={{cn({class_name})}} {props_attr}>"])


def add_div_close(builder):
    builder.add_lines([f"</div>"])
