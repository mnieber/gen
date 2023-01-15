from .create_widget_spec import create_widget_spec


class WidgetSpecParser:
    def __init__(self, module_name, widget_reg=None):
        self.module_name = module_name
        self.widget_reg = widget_reg

    def parse(self, spec_dict, parent_widget_spec=None):
        is_top_level = parent_widget_spec is None
        if is_top_level and self.widget_reg:
            if states := spec_dict.get("__states__"):
                self.widget_reg.states_by_module_name[self.module_name] = states

        items = [
            (key.strip(), value)
            for key, value in spec_dict.items()
            if not _is_private_member(key)
        ]

        for key, value in items:
            widget_spec, spec = create_widget_spec(
                key, value, module_name=self.module_name
            )

            # Update parent/child relationships
            if parent_widget_spec:
                widget_spec.parent = parent_widget_spec
                parent_widget_spec.child_widget_specs.append(widget_spec)

            self._check_top_level_constraints(is_top_level, widget_spec)

            if widget_spec.is_component_def and self.widget_reg:
                if self.widget_reg.get(widget_spec.widget_name, None) is not None:
                    raise Exception(
                        f"Duplicate widget component spec: {widget_spec.widget_name}"
                    )
                self.widget_reg.setdefault(widget_spec.widget_name, widget_spec)

            #
            # Use recursion to convert child widget specs
            #
            if spec:
                self.parse(spec, parent_widget_spec=widget_spec)

    def _check_top_level_constraints(self, is_top_level, widget_spec):
        if is_top_level and not widget_spec.is_component_def:
            raise Exception(
                "The top-level can only have component definitions: "
                + (widget_spec.widget_name or "")
            )


def _is_private_member(key):
    return key.startswith("__")
