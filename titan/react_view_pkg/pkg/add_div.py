import os

from titan.widgets_pkg.pkg.div import Div


def get_div_open(div: Div, widget_class_name=None):
    class_name_attr = div.get_class_name_attr(widget_class_name)
    props_attr = os.linesep.join(div.attrs)

    key = div.key
    key_attr = f"key={{{key}}}" if key else ""
    return f"<div {key_attr} {class_name_attr} {props_attr}>"


def get_div_close():
    return f"</div>"
