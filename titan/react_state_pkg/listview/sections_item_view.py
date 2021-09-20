import os

from moonleap.resources.type_spec_store import type_spec_store


class Sections:
    def __init__(self, res):
        self.res = res

    def fields(self):
        result = []

        type_spec = type_spec_store().get(self.res.item_name)
        for field_spec in type_spec.field_specs:
            if (
                field_spec.private
                or field_spec.name in ("id",)
                or field_spec.field_type in ("slug",)
            ):
                continue
            result.append(
                f"<div>{field_spec.name}: {{props.{self.res.item_name}.{field_spec.name} }}</div>"
            )
        return os.linesep.join(" " * 6 + line for line in result)
