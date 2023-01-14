from titan.react_view_pkg.pkg.get_data_path import get_data_path
from titan.react_view_pkg.pkg.get_named_data_term import get_named_item


class ItemHelper:
    def __init__(self, widget_spec):
        self.widget_spec = widget_spec
        self._named_item = None
        self._working_item_name = None
        self._has_data = False

    @property
    def named_item(self):
        if not self._has_data:
            self._get_data()

        return self._named_item

    @property
    def working_item_name(self):
        if not self._has_data:
            self._get_data()

        return self._working_item_name

    def _get_data(self):
        self._has_data = True
        self._named_item = get_named_item(self.widget_spec)
        if self._named_item:
            self._working_item_name = self.named_item.meta.term.data

    def item_data_path(self):
        named_item = get_named_item(self.widget_spec)
        return get_data_path(self.widget_spec, obj=named_item) if named_item else None
