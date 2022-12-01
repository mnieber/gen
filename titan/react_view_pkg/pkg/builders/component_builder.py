from titan.react_view_pkg.pkg.builder import Builder


class ComponentBuilder(Builder):
    def build(self, classes=None, handlers=None):
        from titan.react_view_pkg.pkg.builders.array_builder import ArrayBuilder

        attrs = []
        component = self.widget_spec.component
        for pipeline in component.pipelines:
            if pipeline.root_props:
                named_input = pipeline.elements[0].obj
                required_prop_name = named_input.name or named_input.typ.ts_var

                if isinstance(self.parent_builder, ArrayBuilder) and (
                    self.parent_builder.item_list.item is named_input.typ
                ):
                    provided_prop_name = required_prop_name
                    attrs += [f"key={{{provided_prop_name}.id}}"]
                else:
                    root_component = self.root_builder.widget_spec.component
                    pipeline, expr = root_component.get_pipeline_and_expr(named_input)
                    provided_prop_name = expr

                attrs += [f"{required_prop_name}={{{provided_prop_name}}}"]

        attrs_str = " ".join(attrs)
        self.add_lines([f"<{self.output.widget_class_name} {attrs_str} />"])
