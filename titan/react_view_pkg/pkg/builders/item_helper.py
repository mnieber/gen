from moonleap import kebab_to_camel
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

    def maybe_add_item_pipeline_to_spec_extension(self, extension):
        pipelines = extension.setdefault("__pipelines__", {})
        if self.widget_spec.get_pipeline_by_name("item", recurse=True):
            return True
        named_props = self.widget_spec.root.get_named_props(
            lambda x: x.meta.term.tag == "item"
        )
        if len(named_props) != 1:
            return False
        pipelines["item"] = ["component:props", str(named_props[0].meta.term)]
        return True

    def maybe_add_save_pipeline_to_spec_extension(self, extension):
        pipelines = extension.setdefault("__pipelines__", {})
        if self.widget_spec.get_pipeline_by_name("save", recurse=True):
            return True
        named_props = self.widget_spec.root.get_named_props(
            lambda x: x.meta.term.tag == "editing"
        )
        if len(named_props) != 1:
            return False
        pipelines["save"] = ["component:props", str(named_props[0].meta.term)]
        return True
