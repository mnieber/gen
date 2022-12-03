from moonleap.utils.fp import append_uniq, uniq


def get_helpers(_):
    class Helpers:
        view = _.component
        widget_spec = _.component.widget_spec
        builder = view.builder
        queries = list()
        mutations = list()
        pipelines = _.component.pipelines
        child_components = builder.output.child_components
        has_children = builder.output.has_children
        build = None

        def __init__(self):
            self._get_queries_from_pipelines()
            self.build = self._get_div()

        def _get_queries_from_pipelines(self):
            for pipeline in self.pipelines:
                pipeline_source = pipeline.source
                if pipeline_source.meta.term.tag == "query":
                    append_uniq(self.queries, pipeline_source)
                if pipeline_source.meta.term.tag == "mutation":
                    append_uniq(self.mutations, pipeline_source)

        def _get_div(self):
            x = self.widget_spec
            self.builder.build()
            return self.builder.output

        @property
        def type_specs_to_import(self):
            result = uniq(
                [
                    res.item.type_spec if res.meta.term.tag == "item~list" else res
                    for res in [x.typ for x in _.component.named_props]
                ]
            )
            return result

    return Helpers()
