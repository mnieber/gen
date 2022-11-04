from dataclasses import dataclass

from moonleap import Resource
from titan.api_pkg.gqlregistry import get_gql_reg


@dataclass
class Container(Resource):
    name: str

    @property
    def delete_items_mutation(self):
        if not self.get_bvr("deletion"):
            return None

        for mutation in get_gql_reg().mutations:
            for item_list_deleted in mutation.item_lists_deleted:
                if self.item_name == item_list_deleted.item.item_name:
                    return mutation

        return None

    @property
    def order_items_mutation(self):
        if not self.get_bvr("insertion"):
            return None

        for mutation in get_gql_reg().mutations:
            for item_list_ordered in mutation.item_lists_ordered:
                if self.item_name == item_list_ordered.item.item_name:
                    return mutation

        return None

    @property
    def delete_item_mutation(self):
        if not self.get_bvr("deletion"):
            return None

        for mutation in get_gql_reg().mutations:
            for item_deleted in mutation.items_deleted:
                if self.item_name == item_deleted.item_name:
                    return mutation

        return None
