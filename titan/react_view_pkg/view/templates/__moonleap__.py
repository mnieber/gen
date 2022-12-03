from moonleap.utils.fp import append_uniq, uniq
from titan.react_view_pkg.pkg.get_builder import get_builder


def get_helpers(_):
    class Helpers:
        view = _.component
        widget_spec = _.component.widget_spec
        queries = list()
        mutations = list()
        pipelines = _.component.pipelines
        build = None

        def __init__(self):
            self._get_queries_from_pipelines()
            self.build = self._get_div(self.widget_spec)

        def _get_queries_from_pipelines(self):
            for pipeline in self.pipelines:
                pipeline_source = pipeline.source
                if pipeline_source.meta.term.tag == "query":
                    append_uniq(self.queries, pipeline_source)
                if pipeline_source.meta.term.tag == "mutation":
                    append_uniq(self.mutations, pipeline_source)

        def _get_div(self, widget_spec, level=0):
            builder = get_builder(widget_spec, None, level)
            builder.build()
            return builder.output

        @property
        def type_specs_to_import(self):
            return uniq(
                [
                    res.item.type_spec if res.meta.term.tag == "item~list" else res
                    for res in _.component.props
                ]
            )

    return Helpers()
