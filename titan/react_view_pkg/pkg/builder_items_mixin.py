from titan.react_view_pkg.pkg.get_data_path import get_data_path
from titan.react_view_pkg.pkg.get_named_data_term import (
    get_named_item_list_term,
    get_named_item_term,
)


class BuilderItemsMixin:
    def item_list_data_path(self):
        term = get_named_item_list_term(self.widget_spec)
        return get_data_path(self.widget_spec, term=term) if term else None

    def item_data_path(self):
        term = get_named_item_term(self.widget_spec)
        return get_data_path(self.widget_spec, term=term) if term else None
