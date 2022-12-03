class BuilderItemsMixin:
    def _get_data_path(self, term):
        if not term:
            return None

        data_path = self.get_data_path(term=term)
        if not data_path:
            raise Exception(f"Could not find data path for: {term}")
        return data_path

    def item_list_data_path(self):
        return self._get_data_path(self.widget_spec.named_items_term)

    def item_data_path(self):
        return self._get_data_path(self.widget_spec.named_item_term)
