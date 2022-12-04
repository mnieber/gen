import ramda as R


def get_helpers(_):
    def _find_behavior(name):
        return R.find(lambda x: x.name == name)(_.component.bvrs)

    class Helpers:
        widget_spec = _.component.widget_spec
        builder = _.component.builder
        child_components = builder.output.child_components
        has_children = builder.output.has_children
        item_name = _.component.item.item_name
        selection_bvr = _find_behavior("selection")
        deletion_bvr = _find_behavior("deletion")
        highlight_bvr = _find_behavior("highlight")
        drag_and_drop_bvr = _find_behavior("dragAndDrop")
        build = None

        has_selection = selection_bvr
        has_highlight = selection_bvr or highlight_bvr
        has_drag_and_drop = drag_and_drop_bvr

        def __init__(self):
            self.build = self.builder.output

    return Helpers()
