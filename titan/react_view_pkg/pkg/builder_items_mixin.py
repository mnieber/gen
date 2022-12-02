import ramda as R

from moonleap.parser.term import Term, word_to_term
from titan.types_pkg.typeregistry import get_type_reg


class BuilderItemsMixin:
    @property
    def named_items_term(self):
        items_str = self.widget_spec.values.get("items")
        if not items_str:
            return None
        result = word_to_term(items_str)
        return result

    @property
    def named_item_term(self):
        item_str = self.widget_spec.values.get("item")
        if not item_str:
            return None
        result = word_to_term(item_str)
        return result

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

    def item_list_expr(self):
        named_items_term = self.named_items_term
        if not named_items_term:
            return None

        item_list_expr = self.parent_builder.get_pipeline_expr(term=named_items_term)
        if not item_list_expr:
            raise Exception(f"Could not find pipeline for: {named_items_term}")
        return item_list_expr

    def item_expr(self):
        named_item_term = self.named_item_term
        if not named_item_term:
            return None

        item_expr = self.parent_builder.get_pipeline_expr(term=named_item_term)
        if not item_expr:
            raise Exception(f"Could not find pipeline for: {named_item_term}")
        return item_expr
