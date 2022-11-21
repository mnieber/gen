from moonleap.utils.split_non_empty import split_non_empty

from .get_widget_spec import get_widget_spec


class WidgetSpecParser:
    def __init__(self, widget_reg):
        self.widget_reg = widget_reg

    def parse(self, widget_spec_dict, parent_widget_spec=None):
        items = [x for x in widget_spec_dict.items() if not _is_private_member(x[0])]

        for key, value in items:
            spec = {} if value == "pass" else value
            is_dict = isinstance(spec, dict)

            widget_spec = get_widget_spec(
                key,
                value_parts=split_non_empty(
                    spec.get("__type__", "") if is_dict else value, "."
                ),
            )

            if widget_spec.is_component:
                if self.widget_reg.get(widget_spec.widget_type, None) is not None:
                    raise Exception(
                        f"Duplicate widget component spec: {widget_spec.widget_type}"
                    )
                self.widget_reg.setdefault(widget_spec.widget_type, widget_spec)

            if parent_widget_spec:
                parent_widget_spec.child_widget_specs.append(widget_spec)

            #
            # Use recursion to convert child widget specs
            #
            if is_dict and spec:
                self.parse(spec, parent_widget_spec=widget_spec)


def _is_private_member(key):
    return key.startswith("__")
