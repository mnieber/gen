from moonleap.utils.fp import append_uniq
from titan.widgetspec.get_scss_styles_by_class_name import get_scss_styles_by_class_name


def get_helpers(_):
    class Helpers:
        view = _.component
        widget_spec = _.component.widget_spec
        build = view.build_output
        queries = list()
        mutations = list()
        pipelines = widget_spec.pipelines
        has_children_prop = widget_spec.has_tag("has_children_prop")
        has_scss = not widget_spec.has_tag("no_scss")
        has_default_props = bool(build.default_props) or not widget_spec.values.get(
            "noDps"
        )
        has_click_handler = "click:handler" in widget_spec.handler_terms

        def __init__(self):
            self._get_queries_from_pipelines()
            self.scss_styles_by_class_name = get_scss_styles_by_class_name(
                self.widget_spec
            )

        def _get_queries_from_pipelines(self):
            for pipeline in self.pipelines:
                pipeline_source = pipeline.source
                if pipeline_source.meta.term.tag == "query":
                    append_uniq(self.queries, pipeline_source)
                if pipeline_source.meta.term.tag == "mutation":
                    append_uniq(self.mutations, pipeline_source)

    return Helpers()
