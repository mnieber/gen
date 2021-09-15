from moonleap.resources.type_spec_store import type_spec_store
from moonleap.utils.case import lower0

from .props_query import _find_module_that_provides_item_list


class SectionsDataType:
    def __init__(self, res):
        self.res = res

    def imports(self, item_name):
        module = _find_module_that_provides_item_list(
            self.res.service.django_app, item_name
        )
        return f"from {module.name}.models import {item_name}"

    def exclude(self, item_name):
        type_spec = type_spec_store.get(item_name)
        list_str = ", ".join(
            [
                f'"{x.name_snake}"'
                for x in type_spec.field_spec_by_name.values()
                if x.private
            ]
        )
        return f"exclude = [{list_str}]" if list_str else ""
