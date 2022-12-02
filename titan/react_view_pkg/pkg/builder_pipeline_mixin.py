class BuilderPipelineMixin:
    def get_pipeline_expr(self, named_output=None, term=None):
        from titan.react_view_pkg.pkg.builders.array_builder import ArrayBuilder

        b = self
        while b:
            component = b.widget_spec.component
            if component:
                pipeline, expr = component.get_pipeline_and_expr(
                    named_output=named_output, term=term
                )
                if pipeline:
                    return expr
            if isinstance(b, ArrayBuilder):
                if (named_output and named_output.typ is b.item_list.item) or (
                    term
                    and term.as_normalized_str
                    == b.item_list.item.meta.term.as_normalized_str
                ):
                    return named_output.typ.ts_var
            b = b.parent_builder
        return None
