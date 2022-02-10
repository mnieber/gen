import os

import ramda as R
from moonleap.typespec.type_spec_store import type_spec_store


def get_context(list_view):
    def _find_behavior(name):
        return R.find(lambda x: x.name == name)(list_view.behaviors)

    _ = lambda: None
    _.type_spec = type_spec_store().get(list_view.item.item_type.name)
    _.selection_bvr = _find_behavior("selection")
    _.deletion_bvr = _find_behavior("deletion")
    _.highlight_bvr = _find_behavior("highlight")

    class Sections:
        def fields(self):
            result = []

            for field_spec in _.type_spec.field_specs:
                if (
                    field_spec.private
                    or field_spec.name in ("id",)
                    or field_spec.field_type in ("slug", "fk", "relatedSet")
                ):
                    continue

                if field_spec.field_type in ("boolean"):
                    value = (
                        f"props.{list_view.item_name}.{field_spec.name} ? 'Yes' : 'No'"
                    )
                else:
                    value = f"props.{list_view.item_name}.{field_spec.name}"

                result.append(f"<div>{field_spec.name}: {{{value}}}</div>")
            return os.linesep.join(" " * 6 + line for line in result)

    return dict(sections=Sections(), _=_)
