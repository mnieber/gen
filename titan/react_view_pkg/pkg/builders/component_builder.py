from moonleap.utils.fp import append_uniq
from titan.react_view_pkg.pkg.builder import Builder
from titan.react_view_pkg.pkg.get_data_path import get_data_path


class ComponentBuilder(Builder):
    def __post_init__(self):
        self.component = self.widget_spec.component

    def build(self):
        self._add_component_import_path()

        attrs = list(self.widget_spec.div_props)
        for pipeline in self.component.pipelines:
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

    def _add_component_import_path(self):
        is_same_module = (
            self.widget_spec.module_name == self.widget_spec.parent.module_name
        )
        suffix = f"/{self.component.name}" if is_same_module else ""
        append_uniq(
            self.output.import_lines,
            f"import {{ {self.component.name} }} from "
            + f"'src/{self.component.module.module_path}/components{suffix}';",
        )
