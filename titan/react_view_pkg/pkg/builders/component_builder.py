from moonleap.utils.fp import append_uniq
from titan.react_view_pkg.pkg.builder import Builder
from titan.react_view_pkg.pkg.get_data_path import get_data_path


class ComponentBuilder(Builder):
    def build(self):
        component = self.widget_spec.component
        append_uniq(self.output.child_components, component)

        attrs = list(self.widget_spec.div_props)
        for pipeline in component.pipelines:
            if pipeline.root_props:
                named_input = pipeline.elements[0].obj
                required_prop_name = named_input.name or named_input.typ.ts_var
                # The required prop must be supplied by some parent component
                data_path = get_data_path(
                    self.widget_spec.parent, term=named_input.meta.term
                )
                attrs += [f"{required_prop_name}={{{data_path}}}"]
        attrs_str = " ".join(attrs)

        key = self.widget_spec.div_key
        key_attr = f"key={{{key}}}" if key else ""
        self.add_lines(
            [f"<{self.widget_spec.widget_class_name} {key_attr} {attrs_str}/>"]
        )
