import ramda as R


def get_helpers(_):
    def _find_behavior(name):
        return R.find(lambda x: x.name == name)(_.component.bvrs)

    class Helpers:
        type_spec = _.component.item.type_spec
        selection_bvr = _find_behavior("selection")
        deletion_bvr = _find_behavior("deletion")
        highlight_bvr = _find_behavior("highlight")

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
