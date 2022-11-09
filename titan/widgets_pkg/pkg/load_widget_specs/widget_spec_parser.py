from .get_widget_spec import get_widget_spec


class WidgetSpecParser:
    def __init__(self, widget_reg):
        self.widget_reg = widget_reg

    def parse(self, widget_spec_dict, parent_widget_spec=None):
        items = [x for x in widget_spec_dict.items() if not _is_private_member(x[0])]

        for key, value in items:
            spec = {} if value == "pass" else value
            is_dict = isinstance(spec, dict)

            if is_dict:
                widget_spec = get_widget_spec(key, spec)
            else:
                if not parent_widget_spec:
                    raise Exception(
                        f"The root widget spec can only contain widget specs"
                    )

                widget_spec = get_widget_spec(key, {})
                values = value if isinstance(spec, list) else spec.split(".")
                widget_spec.values.extend(values)

            if widget_spec.is_component:
                if self.widget_reg.get(widget_spec.widget_name, None) is not None:
                    raise Exception(
                        f"Duplicate widget component spec: {widget_spec.widget_name}"
                    )
                self.widget_reg.setdefault(widget_spec.widget_name, widget_spec)

            if parent_widget_spec:
                parent_widget_spec.child_widget_specs.append(widget_spec)

            #
            # Use recursion to convert child widget specs
            #
            if is_dict and spec:
                self.parse(spec, parent_widget_spec=widget_spec)


def _is_private_member(key):
    return key.startswith("__")
