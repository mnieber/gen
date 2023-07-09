from moonleap.utils.inflect import plural


class BvrsHelper:
    def __init__(self, item_name):
        assert item_name
        self.bvrs_items_name = plural(item_name)

        self.bvr_names = self.get_bvr_names(recurse=True)
        self.bvrs_has_addition = "addition" in self.bvr_names
        self.bvrs_has_deletion = "deletion" in self.bvr_names
        self.bvrs_has_drag_and_drop = "dragAndDrop" in self.bvr_names
        self.bvrs_has_highlight = "highlight" in self.bvr_names
        self.bvrs_has_selection = "selection" in self.bvr_names

    def bvrs_context(self):
        return {
            "bvrs_has_addition": self.bvrs_has_addition,
            "bvrs_has_deletion": self.bvrs_has_deletion,
            "bvrs_has_drag_and_drop": self.bvrs_has_drag_and_drop,
            "bvrs_has_highlight": self.bvrs_has_highlight,
            "bvrs_has_selection": self.bvrs_has_selection,
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
