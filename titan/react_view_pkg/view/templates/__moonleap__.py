from moonleap.utils.fp import append_uniq, uniq


def get_helpers(_):
    class Helpers:
        view = _.component
        widget_spec = _.component.widget_spec
        builder = view.builder
        queries = list()
        mutations = list()
        pipelines = _.component.pipelines
        has_children = builder.output.has_children
        build = None

        def __init__(self):
            self._get_queries_from_pipelines()
            self.build = self.builder.output

        def _get_queries_from_pipelines(self):
            for pipeline in self.pipelines:
                pipeline_source = pipeline.source
                if pipeline_source.meta.term.tag == "query":
                    append_uniq(self.queries, pipeline_source)
                if pipeline_source.meta.term.tag == "mutation":
                    append_uniq(self.mutations, pipeline_source)

        @property
        def type_specs_to_import(self):
            return []

    return Helpers()
