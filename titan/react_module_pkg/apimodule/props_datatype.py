import os

from moonleap import upper0
from moonleap.resources.type_spec_store import type_spec_store
from moonleap.utils.case import lower0


def _fields(type_spec):
    return [
        (field_name, field_spec)
        for field_name, field_spec in type_spec.field_spec_by_name.items()
        if not field_spec.private
    ]


class SectionsDataType:
    def __init__(self, res):
        self.res = res

    def schema_imports(self, item_name):
        result = []

        type_spec = type_spec_store.get(upper0(item_name))
        for field_name, field_spec in _fields(type_spec):
            if field_spec.field_type in ("list", "related_set", "item", "fk"):
                fk_item_name = lower0(field_spec.fk_type_spec.type_name)
                result.append(
                    f"import {{ {fk_item_name} }} from 'src/api/types/{fk_item_name}';"
                )

        return os.linesep.join(result)

    def define_fields(self, item_name):
        result = []
        tab = " " * 2

        type_spec = type_spec_store.get(upper0(item_name))
        for field_name, field_spec in _fields(type_spec):
            if field_spec.field_type in ("list", "related_set"):
                fk_item_name = lower0(field_spec.fk_type_spec.type_name)
                result.append(
                    f"{item_name}.define({{ {field_name}: [{fk_item_name}] }});"
                )

            if field_spec.field_type in ("item", "fk"):
                fk_item_name = lower0(field_spec.fk_type_spec.type_name)
                result.append(
                    f"{item_name}.define({{ {field_name}: {fk_item_name} }});"
                )

        return ("," + os.linesep).join(result)
