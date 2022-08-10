import os

import ramda as R


def get_helpers(_):
    def _find_behavior(name):
        return R.find(lambda x: x.name == name)(_.component.bvrs)

    class Helpers:
        type_spec = _.component.item.item_type.type_spec
        selection_bvr = _find_behavior("selection")
        deletion_bvr = _find_behavior("deletion")
        highlight_bvr = _find_behavior("highlight")

        def fields(self):
            result = []

            for field_spec in self.type_spec.field_specs:
                if (
                    field_spec.private
                    or field_spec.name in ("id",)
                    or field_spec.field_type in ("slug", "fk", "relatedSet")
                ):
                    continue

                if field_spec.field_type in ("boolean"):
                    value = f"props.{_.component.item_name}.{field_spec.name} ? 'Yes' : 'No'"
                else:
                    value = f"props.{_.component.item_name}.{field_spec.name}"

                result.append(f"<div>{field_spec.name}: {{{value}}}</div>")
            return os.linesep.join(" " * 6 + line for line in result)

    return Helpers()
