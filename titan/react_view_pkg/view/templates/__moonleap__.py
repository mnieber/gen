from moonleap.utils.fp import append_uniq


def get_helpers(_):
    class Helpers:
        view = _.component
        widget_spec = _.component.widget_spec
        build = view.build_output
        queries = list()
        mutations = list()
        pipelines = _.component.pipelines
        has_children = build.has_children
        has_scss = not build.no_scss

        def __init__(self):
            self._get_queries_from_pipelines()

        def _get_queries_from_pipelines(self):
            for pipeline in self.pipelines:
                pipeline_source = pipeline.source
                if pipeline_source.meta.term.tag == "query":
                    append_uniq(self.queries, pipeline_source)
                if pipeline_source.meta.term.tag == "mutation":
                    append_uniq(self.mutations, pipeline_source)

        @property
        def type_specs_to_import(self):
            result = []
            for named_prop in self.view.named_props:
                if named_prop.meta.term.tag in ("item",):
                    append_uniq(result, named_prop.typ.type_spec)
                if named_prop.meta.term.tag in ("item~list",):
                    append_uniq(result, named_prop.typ.item.type_spec)
            return result

    return Helpers()
