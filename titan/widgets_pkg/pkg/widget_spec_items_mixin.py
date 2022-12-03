import ramda as R

from moonleap.parser.term import Term, match_term_to_pattern, word_to_term
from titan.types_pkg.typeregistry import get_type_reg


class WidgetSpecItemsMixin:
    def get_value_by_name(self, name):
        ws = self
        while ws:
            value = ws.values.get(name)
            if value:
                return value
            ws = ws.parent
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
