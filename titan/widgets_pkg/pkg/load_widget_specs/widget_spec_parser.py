from .get_widget_spec import get_widget_spec


class WidgetSpecParser:
    def __init__(self, widget_spec_dict, module_name, widget_reg=None):
        self.widget_spec_dict = widget_spec_dict
        self.module_name = module_name
        self.widget_reg = widget_reg

    def parse(self, spec_dict=None, parent_widget_spec=None, level=0):
        from titan.react_view_pkg.pkg.get_builders import get_builders

        assert spec_dict is not None or level == 0
        spec_dict = self.widget_spec_dict if spec_dict is None else spec_dict

        if level == 0 and self.widget_reg:
            if states := spec_dict.get("__states__"):
                self.widget_reg.states_by_module_name[self.module_name] = states

        items = [
            (key.strip(), value)
            for key, value in spec_dict.items()
            if not _is_private_member(key)
        ]

        for key, value in items:
            widget_spec, spec = get_widget_spec(
                key, value, module_name=self.module_name
            )

            # Update parent/child relationships
            if parent_widget_spec:
                widget_spec.parent_ws = parent_widget_spec
                parent_widget_spec.child_widget_specs.append(widget_spec)

            # Create builders for this widget spec
            builders = get_builders(widget_spec)

            # Every builder has the option to update the created widget-spec.
            for builder in builders:
                builder.update_widget_spec()

            # Every builder has the option to extend the spec before we continue
            # to process it.
            for builder in builders:
                extension = builder.get_spec_extension(_get_places(spec))
                spec.update(extension or {})

            self._check_top_level_constraints(level, widget_spec)

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
                self.parse(
                    spec,
                    parent_widget_spec=widget_spec,
                    level=level + 1,
                )

    def _check_top_level_constraints(self, level, widget_spec):
        if level == 0 and not widget_spec.is_component_def:
            raise Exception(
                "The top-level can only have component definitions: "
                + (widget_spec.widget_name or "")
            )


def _is_private_member(key):
    return key.startswith("__")


def _get_places(spec):
    places = []
    for key in spec.keys():
        parts = key.split(" with ")
        if len(parts) == 2 and key.startswith(parts[0] + " with "):
            places.append(parts[0])

    return places
