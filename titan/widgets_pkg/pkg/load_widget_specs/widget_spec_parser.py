from .get_widget_spec import get_widget_spec


class WidgetSpecParser:
    def __init__(self, widget_spec_dict, module_name, widget_reg=None):
        self.widget_spec_dict = widget_spec_dict
        self.module_name = module_name
        self.widget_reg = widget_reg
        # This member stores automatically suggested widget specs (that are returned by
        # the call to get_spec_extension)
        self.auto_spec = {}
        self.auto_spec_widget_names = []

    def parse(
        self, spec_dict=None, parent_widget_spec=None, parent_builder=None, level=0
    ):
        from titan.react_view_pkg.pkg.get_builder import get_builder

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
                assert parent_builder

                # The parent builder has the option to update the widget-spec
                # that is used in one of its places.
                if widget_spec.place:
                    parent_builder.update_place(widget_spec)

                widget_spec.parent_ws = parent_widget_spec
                parent_widget_spec.child_widget_specs.append(widget_spec)

            # The builder has the option to extend the spec before we continue
            # to process it.
            builder = None
            if widget_spec.widget_base_type:
                builder = get_builder(widget_spec)
                extension = builder.get_spec_extension(_get_places(spec))
                self._handle_spec_extension(spec, extension)

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
            if isinstance(spec, dict):
                self.parse(
                    spec,
                    parent_widget_spec=widget_spec,
                    parent_builder=builder,
                    level=level + 1,
                )

        if level == 0 and self.auto_spec:
            new_spec_dict = self.auto_spec
            self.auto_spec = {}
            self.parse(new_spec_dict)

    def _check_top_level_constraints(self, level, widget_spec):
        if widget_spec.is_component_def and level > 0:
            raise Exception(
                "Component definitions must be top-level: "
                + (widget_spec.widget_name or "")
            )

        if level == 0 and not widget_spec.is_component_def:
            raise Exception(
                "The top-level can only have component definitions: "
                + (widget_spec.widget_name or "")
            )

    def _handle_spec_extension(self, spec, extension):
        for k, v in (extension or {}).items():
            extra_widget_spec, extra_spec = get_widget_spec(
                k, v, module_name=self.module_name
            )
            if extra_widget_spec.place:
                spec[k] = v
            elif extra_widget_spec.is_component_def and (
                extra_widget_spec.widget_name not in self.auto_spec_widget_names
            ):
                self.auto_spec_widget_names.append(extra_widget_spec.widget_name)
                self.auto_spec[k] = v


def _is_private_member(key):
    return key.startswith("__")


def _get_places(spec):
    places = []
    for key in spec.keys():
        parts = key.split(" with ")
        if len(parts) == 2 and key.startswith(parts[0] + " with "):
            places.append(parts[0])

    return places
