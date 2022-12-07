from moonleap.parser.term import word_to_term
from titan.react_view_pkg.pkg.get_data_path import get_data_path


class BuilderItemsMixin:
    def get_value_by_name(self, name, default=None):
        ws = self.widget_spec
        while ws:
            value = ws.values.get(name)
            if value:
                return value
            ws = ws.parent_ws
        return default

    def get_named_data_term(self, name):
        value = self.get_value_by_name(name)
        if value and "+" not in value:
            raise Exception(f"Expected + in value: {value}")
        return word_to_term(value) if value else None

    @property
    def named_item_list_term(self):
        return self.get_named_data_term("items")

    @property
    def named_item_term(self):
        return self.get_named_data_term("item")

    def _get_data_path(self, term):
        if not term:
            return None

        return get_data_path(self.widget_spec, term=term)

    def item_list_data_path(self):
        return self._get_data_path(self.named_item_list_term)

    def item_data_path(self):
        return self._get_data_path(self.named_item_term)
