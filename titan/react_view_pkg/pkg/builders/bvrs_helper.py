from moonleap.utils.inflect import plural


class BvrsHelper:
    def __init__(self, widget_spec, item_name):
        assert item_name
        self.widget_spec = widget_spec
        self.bvrs_items_name = plural(item_name)

        self.bvrs = self.widget_spec.get_bvr_names(recurse=True)
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
