from moonleap import kebab_to_camel
from titan.react_view_pkg.pkg.get_data_path import get_data_path


class ItemListHelper:
    def __init__(self, widget_spec):
        self.widget_spec = widget_spec
        self._named_item_list = None
        self._working_item_name = None
        self._has_data = False

    @property
    def named_item_list(self):
        if not self._has_data:
            self._get_data()

        return self._named_item_list

    @property
    def working_item_name(self):
        if not self._has_data:
            self._get_data()

        return self._working_item_name

    def _get_data(self):
        self._has_data = True
        if pipeline := self.widget_spec.get_pipeline_by_name("items", recurse=True):
            self._named_item_list = pipeline.resources[-1]
            self._working_item_name = kebab_to_camel(
                self._named_item_list.meta.term.data
            )

    def item_list_data_path(self):
        return (
            get_data_path(self.widget_spec, obj=self.named_item_list)
            if self.named_item_list
            else None
        )

    def maybe_add_item_pipeline_to_spec_extension(self, extension):
        pipelines = extension.setdefault("__pipelines__", {})
        if self.widget_spec.get_pipeline_by_name("item", recurse=True):
            return True
        item_name = self.working_item_name
        pipelines["item"] = ["local:vars", f"{item_name}+{item_name}:item"]
        return True

    def maybe_add_items_pipeline_to_spec_extension(self, extension):
        pipelines = extension.setdefault("__pipelines__", {})
        if self.widget_spec.get_pipeline_by_name("items", recurse=True):
            return True
        named_props = self.widget_spec.root.get_named_props(
            lambda x: x.meta.term.tag == "item~list"
        )
        if len(named_props) != 1:
            return False
        pipelines["items"] = ["component:props", str(named_props[0].meta.term)]
        return True
