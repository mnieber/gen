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

    def get_spec_extension(self):
        pipelines = self.widget_spec.src_dict.get("__pipelines__", {})
        # The widget_spec for the component should have a pipeline for the item
        # that returns a data-path to the local variable that holds the item.
        if "item" not in pipelines.keys():
            item_name = self.working_item_name
            return dict(
                __pipelines__=dict(item=["local:vars", f"{item_name}+{item_name}:item"])
            )
        return None
