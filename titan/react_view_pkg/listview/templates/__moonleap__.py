def get_helpers(_):
    class Helpers:
        view = _.component
        item_name = view.item_list.item_name
        has_key_handler = bool(view.key_handler)
        has_selection = bool(view.selection_bvr)
        has_highlight = bool(view.highlight_bvr)
        has_drag_and_drop = bool(view.drag_and_drop_bvr)

        def __init__(self):
            pass

    return Helpers()
