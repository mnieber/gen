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
