import ramda as R

from moonleap.parser.term import Term, match_term_to_pattern, word_to_term
from titan.types_pkg.typeregistry import get_type_reg


class BuilderItemsMixin:
    def get_value_by_name(self, name):
        b = self
        while b:
            value = b.widget_spec.values.get(name)
            if value:
                return value
            b = b.parent_builder
        return None

    def get_named_data_term(self, name):
        value = self.get_value_by_name(name)
        if value and "+" not in value:
            raise Exception(f"Expected + in value: {value}")
        return word_to_term(value) if value else None

    @property
    def named_items_term(self):
        return self.get_named_data_term("items")

    @property
    def named_item_term(self):
        return self.get_named_data_term("item")

    @property
    def item_list(self):
        named_items_term = self.named_items_term
        if not named_items_term:
            return None

        items_term = Term(data=named_items_term.data, tag=named_items_term.tag)
        return R.head(
            item.item_list
            for item in get_type_reg().items
            if match_term_to_pattern(item.item_list.meta.term, items_term)
        )

    @property
    def item(self):
        named_item_term = self.named_item_term
        if not named_item_term:
            return None

        item_term = Term(data=named_item_term.data, tag=named_item_term.tag)
        return R.head(
            item
            for item in get_type_reg().items
            if match_term_to_pattern(item.meta.term, item_term)
        )

    def _get_data_path(self, term):
        if not term:
            return None

        data_path = self.parent_builder.get_data_path(term=term)
        if not data_path:
            raise Exception(f"Could not find data path for: {term}")
        return data_path

    def item_list_data_path(self):
        return self._get_data_path(self.named_items_term)

    def item_data_path(self):
        return self._get_data_path(self.named_item_term)
