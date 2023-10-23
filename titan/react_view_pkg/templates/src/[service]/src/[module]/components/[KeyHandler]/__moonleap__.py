def get_helpers(_):
    class Helpers:
        view = _.component
        list_view = view.list_view
        main_div = ""
        component_name = list_view.name + "KeyHandler"
        item_name = list_view.item_list.item_name
        has_highlight = bool(list_view.highlight_bvr)
        has_selection = bool(list_view.selection_bvr)

        def __init__(self):
            self.level = 6
            self.render_main_div()

        def render_main_div(self):
            self.main_div = ""

    return Helpers()
    
    
def get_meta_data_by_fn(_, __):
    return {
        "KeyHandler.tsx.j2": {
            "name": f"{__.component_name}.tsx",
        },
    }
