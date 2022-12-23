from moonleap import kebab_to_camel
from titan.react_view_pkg.pkg.get_data_path import get_data_path
from titan.react_view_pkg.pkg.get_named_data_term import (
    get_named_item,
    get_named_item_list,
)
from widgetspec.widget_spec_pipeline import WsPipeline


class ItemListHelper:
    def __init__(self, widget_spec):
        self.widget_spec = widget_spec
        self._named_item_list = None
        self._array_item_name = None
        self._has_data = False

    @property
    def named_item_list(self):
        if not self._has_data:
            self._get_data()

        return self._named_item_list

    @property
    def array_item_name(self):
        if not self._has_data:
            self._get_data()

        return self._array_item_name

    def _get_data(self):
        self._has_data = True
        self._named_item_list = get_named_item_list(self.widget_spec)
        if self._named_item_list:
            self._array_item_name = kebab_to_camel(self.named_item_list.meta.term.data)

    def item_list_data_path(self):
        return (
            get_data_path(self.widget_spec, obj=self.named_item_list, term=None)
            if self.named_item_list
            else None
        )

    def update_widget_spec(self):
        if not self.named_item_list:
            raise Exception(
                "ItemListHelper.update_widget_spec requires a named item list"
            )

        self.widget_spec.values["item"] = str(
            self.named_item_list.meta.term
        ).removesuffix("~list")
        self.widget_spec.pipelines.append(
            WsPipeline(
                term=get_named_item(self.widget_spec).meta.term,
                term_data_path=self.array_item_name,
            )
        )
