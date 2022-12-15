from moonleap import kebab_to_camel
from moonleap.utils.inflect import plural
from titan.react_view_pkg.pkg.get_named_data_term import get_named_item_list_term


class BvrsBuilderMixin:
    def __init__(self):
        self.named_item_list_term = get_named_item_list_term(self.widget_spec)
        if not self.named_item_list_term:
            raise Exception("BvrsBuilderMixin requires a named item list term")

        self.bvrs_item_name = kebab_to_camel(self.named_item_list_term.data)
        self.bvrs_items_name = plural(self.bvrs_item_name)

        self.bvrs = self.widget_spec.get_value_by_name("bvrs", default="").split(",")
        self.bvrs_has_selection = "selection" in self.bvrs
        self.bvrs_has_highlight = "highlight" in self.bvrs
        self.bvrs_has_drag_and_drop = "dragAndDrop" in self.bvrs
        self.bvrs_has_deletion = "deletion" in self.bvrs

    def bvrs_context(self):
        return {
            "bvrs_has_selection": self.bvrs_has_selection,
            "bvrs_has_highlight": self.bvrs_has_highlight,
            "bvrs_has_drag_and_drop": self.bvrs_has_drag_and_drop,
            "bvrs_has_deletion": self.bvrs_has_deletion,
        }

    def bvrs_default_props(self):
        return (
            []
            + ([f"{self.bvrs_items_name}Selection"] if self.bvrs_has_selection else [])
            + ([f"{self.bvrs_items_name}Highlight"] if self.bvrs_has_highlight else [])
            + (
                [f"{self.bvrs_items_name}DragAndDrop"]
                if self.bvrs_has_drag_and_drop
                else []
            )
            + ([f"{self.bvrs_items_name}Deletion"] if self.bvrs_has_deletion else [])
        )
