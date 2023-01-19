from moonleap import append_uniq, kebab_to_camel
from moonleap.blocks.term import word_to_term


class ItemHelper:
    def __init__(self, widget_spec):
        self.widget_spec = widget_spec
        self._working_item_name = None

    @property
    def working_item_name(self):
        if not self._working_item_name:
            self._get_data()

        return self._working_item_name

    def _get_data(self):
        if pipeline_data := self.widget_spec.get_pipeline_data("item", recurse=True):
            if term := word_to_term(pipeline_data[-1]):
                self._working_item_name = kebab_to_camel(term.data)

    def item_data_path(self):
        if pipeline := self.widget_spec.get_pipeline_by_name("item", recurse=True):
            named_item = pipeline.resources[-1]
            return pipeline.data_path(obj=named_item)
        return None

    def maybe_add_item_pipeline_to_spec_extension(self, source_term_str, extension):
        pipelines = extension.setdefault("__pipelines__", {})
        if not self.widget_spec.get_pipeline_data("item", recurse=True):
            if named_prop_term := self._get_named_prop_term("item"):
                pipelines["item"] = [source_term_str, str(named_prop_term)]
            else:
                return False
        return True

    def maybe_add_save_pipeline_to_spec_extension(self, extension):
        pipelines = extension.setdefault("__pipelines__", {})
        if not self.widget_spec.get_pipeline_data("save", recurse=True):
            if named_prop_term := self._get_named_prop_term("editing"):
                pipelines["save"] = ["component:props", str(named_prop_term)]
            else:
                return False
        return True

    def _get_named_prop_term(self, tag):
        named_prop_terms = get_named_prop_terms(
            self.widget_spec.root, lambda term: term.tag == tag
        )
        if len(named_prop_terms) != 1:
            return None
        return named_prop_terms[0]


def get_named_prop_terms(widget_spec, predicate):
    result = []
    for named_prop in widget_spec.src_dict.get("__props__", []):
        term = word_to_term(named_prop)
        if predicate(term):
            append_uniq(result, term)
    for named_default_prop in widget_spec.src_dict.get("__default_props__", []):
        term = word_to_term(named_default_prop)
        if predicate(term):
            append_uniq(result, term)
    return result
