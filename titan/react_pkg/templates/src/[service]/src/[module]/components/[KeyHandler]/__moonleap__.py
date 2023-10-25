def get_helpers(_):
    class Helpers:
        view = _.component
        list_view = view.list_view
        item_list = list_view.item_list
        item_name = item_list.item_name
        has_highlight = bool(list_view.highlight_bvr)
        has_selection = bool(list_view.selection_bvr)
        component_name = list_view.name + "KeyHandler"
        state = item_list.container.state
        main_div = ""

        def __init__(self):
            self.level = 6
            self.render_main_div()

        def render_main_div(self):
            self.main_div = ""

    return Helpers()


def get_meta_data_by_fn(_, __):
    return {
        ".": {
            "name": "..",
        },
        "KeyHandler.tsx.j2": {
            "name": f"{__.component_name}.tsx",
        },
    }


def get_contexts(_):
    return [
        dict(component=component)
        for component in _.module.components
        if component.meta.term.tag == "key-handler"
    ]
