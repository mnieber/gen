from moonleap.utils.split_non_empty import split_non_empty

from .get_widget_spec import get_widget_spec


class WidgetSpecParser:
    def __init__(self, widget_reg=None):
        self.widget_reg = widget_reg

    def parse(self, widget_spec_dict, parent_widget_spec=None, level=0):
        from titan.react_view_pkg.pkg.get_builder import get_builder

        if level > 1000:
            raise Exception("Infinite loop detected")

        items = [
            (key.strip(), value)
            for key, value in widget_spec_dict.items()
            if not _is_private_member(key)
        ]
        widget_specs = []

        for key, value in items:
            spec = {} if value == "pass" else value
            is_dict = isinstance(spec, dict)

            widget_spec = get_widget_spec(
                key,
                value_parts=split_non_empty(
                    _get_type_value(spec) if is_dict else value, "."
                ),
            )
            widget_spec.parent = parent_widget_spec
            widget_specs.append(widget_spec)

            # Extend spec using the builder for this widget spec
            if widget_spec.widget_base_type:
                spec.update(
                    get_builder(widget_spec).get_spec_extension(_get_places(spec))
                )

            if self.widget_reg and widget_spec.is_component_def:
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
                self.parse(spec, parent_widget_spec=widget_spec, level=level + 1)

        return widget_specs


# Find all keys in spec of type "__attrs__~ " (with k tildes and k spaces)
# and return the concatenated values of these keys
def _get_type_value(spec):
    parts = []
    for key, value in spec.items():
        clean_key = key.strip()
        while clean_key.endswith("~"):
            clean_key = clean_key[:-1].strip()

        if clean_key == "__attrs__":
            parts.append(value)

    return ".".join(parts)


def _is_private_member(key):
    return key.startswith("__")


def _get_places(spec):
    places = []
    for key in spec.keys():
        parts = key.split(" with ")
        if len(parts) == 2 and key.startswith(parts[0] + " with "):
            places.append(parts[0])

    return places
