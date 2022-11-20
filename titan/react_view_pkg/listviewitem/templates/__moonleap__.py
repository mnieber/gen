import ramda as R


def get_helpers(_):
    def _find_behavior(name):
        return R.find(lambda x: x.name == name)(_.component.list_view.bvrs)

    class Helpers:
        widget_spec = _.component.widget_spec
        type_spec = _.component.list_view.item.type_spec
        selection_bvr = _find_behavior("selection")
        deletion_bvr = _find_behavior("deletion")
        highlight_bvr = _find_behavior("deletion")
        drag_and_drop_bvr = _find_behavior("dragAndDrop")

        has_selection = selection_bvr
        has_highlight = selection_bvr or highlight_bvr
        has_drag_and_drop = drag_and_drop_bvr

        @property
        def fields(self):
            result = []

            for field_spec in self.type_spec.get_field_specs():
                if (
                    "client" in field_spec.has_model
                    and field_spec.name not in ("id",)
                    and field_spec.field_type not in ("slug", "fk", "relatedSet")
                ):
                    result.append(field_spec)

            return result

    return Helpers()
