import ramda as R

from moonleap.parser.term import Term, word_to_term
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
            x.item_list
            for x in get_type_reg().items
            if x.item_list.meta.term.as_normalized_str == items_term.as_normalized_str
        )

    @property
    def item(self):
        named_item_term = self.named_item_term
        if not named_item_term:
            return None

        item_term = Term(data=named_item_term.data, tag=named_item_term.tag)
        return R.head(
            x
            for x in get_type_reg().items
            if x.meta.term.as_normalized_str == item_term.as_normalized_str
        )

    def _get_expr(self, term):
        if not term:
            return None

        expr = self.parent_builder.get_pipeline_expr(term=term)
        if not expr:
            raise Exception(f"Could not find pipeline for: {term}")
        return expr

    def item_list_expr(self):
        return self._get_expr(self.named_items_term)

    def item_expr(self):
        return self._get_expr(self.named_item_term)
