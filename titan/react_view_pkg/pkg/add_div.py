import os

from titan.widgetspec.div import Div


def get_div_open(div: Div, widget_class_name=None, also_close=False):
    class_name_attr = div.get_class_name_attr(widget_class_name)
    props_attr = os.linesep.join(div.attrs)

    key = div.key
    key_attr = f"key={{{key}}}" if key else ""
    postfix = " />" if also_close else ">"
    return f"<{div.elm} {key_attr} {class_name_attr} {props_attr}{postfix}"


def get_div_close(div: Div):
    return f"</{div.elm}>"


def add_div_open(builder, also_close=False):
    builder.output.add(
        lines=[
            get_div_open(
                builder.widget_spec.div,
                widget_class_name=builder.widget_spec.widget_class_name,
                also_close=also_close,
            )
        ]
    )


def add_div_close(builder):
    builder.output.add(lines=[get_div_close(builder.widget_spec.div)])
