from moonleap import u0


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


def get_meta_data_by_fn(_, __):
    return {
        "ListView.tsx.j2": {
            "name": f"{u0(_.component.name)}.tsx",
        },
        "ListView.scss.j2": {
            "name": f"{u0(_.component.name)}.scss",
        },
        "ListViewItem.tsx.j2": {
            "name": f"{u0(_.component.name)}Item.tsx",
        },
        "ListViewItem.scss.j2": {
            "name": f"{u0(_.component.name)}Item.scss",
        },
    }


def get_contexts(_):
    return [
        dict(component=component)
        for component in _.module.components
        if component.meta.term.tag == "list-view"
    ]
