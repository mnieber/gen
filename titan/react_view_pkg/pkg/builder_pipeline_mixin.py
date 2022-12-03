from moonleap.parser.term import match_term_to_pattern


class BuilderPipelineMixin:
    def get_data_path(self, named_output=None, term=None):
        from titan.react_view_pkg.pkg.builders.array_builder import ArrayBuilder

        b = self
        while b:
            component = b.widget_spec.component
            if component:
                pipeline, data_path = component.get_pipeline_and_data_path(
                    named_output=named_output, term=term
                )
                if data_path:
                    return data_path
            if isinstance(b, ArrayBuilder):
                if (named_output and named_output.typ is b.item_list.item) or (
                    term and match_term_to_pattern(b.item_list.item.meta.term, term)
                ):
                    return named_output.typ.ts_var
            b = b.parent_builder
        return None
