from dataclasses import dataclass

from moonleap import Resource, u0
from titan.api_pkg.apiregistry import get_api_reg
from titan.types_pkg.typeregistry import get_type_reg


@dataclass
class Container(Resource):
    name: str

    @property
    def delete_items_mutation(self):
        if not self.get_bvr("deletion"):
            return None

        for mutation in get_api_reg().mutations:
            for item_list_deleted in mutation.item_lists_deleted:
                if self.item == item_list_deleted.item:
                    return mutation

        return None

    @property
    def delete_item_mutation(self):
        if not self.get_bvr("deletion"):
            return None

        for mutation in get_api_reg().mutations:
            for item_deleted in mutation.items_deleted:
                if self.item == item_deleted:
                    return mutation

        return None

    @property
    def order_items_mutation(self):
        if not self.get_bvr("insertion"):
            return None

        for mutation in get_api_reg().mutations:
            for parent_type_name, parent_key in mutation.api_spec.orders:
                field_spec = (
                    get_type_reg()
                    .get(u0(parent_type_name))
                    .get_field_spec_by_key(parent_key)
                )

                if self.item.type_spec.type_name == field_spec.target:
                    return mutation

        return None
