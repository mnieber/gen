from moonleap import kebab_to_camel
from titan.react_view_pkg.pkg.hydrate_widget_spec import dps_str_to_term


class ItemListHelper:
    def __init__(self, widget_spec):
        self.widget_spec = widget_spec
        self._working_item_name = None

    @property
    def working_item_name(self):
        if not self._working_item_name:
            self._get_data()

        return self._working_item_name

    def _get_data(self):
        if pipeline := self.widget_spec.get_pipeline_by_name("items", recurse=True):
            named_item_list = pipeline.resources[-1]
            self._working_item_name = named_item_list.typ.item_name

    def item_list_data_path(self):
        if pipeline := self.widget_spec.get_pipeline_by_name("items", recurse=True):
            named_item_list = pipeline.resources[-1]
            return pipeline.data_path(obj=named_item_list)
        return None

    def maybe_add_item_pipeline_to_spec_extension(self, source_term_str, extension):
        pipelines = extension.setdefault("__pipelines__", {})

        if not self.widget_spec.get_pipeline_data("item", recurse=True):
            if value := self.widget_spec.get_value_by_name("item", recurse=True):
                pipelines["item"] = [source_term_str, value]
            else:
                return False

        return True

    def maybe_add_items_pipeline_to_spec_extension(self, extension):
        pipelines = extension.setdefault("__pipelines__", {})
        if not self.widget_spec.get_pipeline_data("items", recurse=True):
            if value := self.widget_spec.get_value_by_name("items", recurse=True):
                pipelines["items"] = ["component:props", value]
            else:
                return False
        return True
