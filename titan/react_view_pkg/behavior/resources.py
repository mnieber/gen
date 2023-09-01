from dataclasses import dataclass

from moonleap import Resource, u0
from titan.api_pkg.apiregistry import get_api_reg
from titan.types_pkg.typeregistry import get_type_reg


@dataclass
class Behavior(Resource):
    name: str
    has_param: bool
    is_skandha: bool = True

    @property
    def mutation(self):
        return None


@dataclass
class EditingBehavior(Behavior):
    @property
    def mutation(self):
        for mutation in get_api_reg().get_mutations():
            for item_saved in mutation.items_saved:
                if (
                    self.container.item_list
                    and self.container.item_name == item_saved.item_name
                ):
                    return mutation


@dataclass
class InsertionBehavior(Behavior):
    @property
    def mutation(self):
        for mutation in get_api_reg().get_mutations():
            for parent_type_name, parent_key in mutation.api_spec.orders:
                field_spec = (
                    get_type_reg()
                    .get(u0(parent_type_name))
                    .get_field_spec_by_key(parent_key)
                )

                if (
                    self.container.item_list
                    and u0(self.container.item_name) == field_spec.target
                ):
                    return mutation


@dataclass
class DeletionBehavior(Behavior):
    @property
    def mutation(self):
        for mutation in get_api_reg().get_mutations():
            for item_list_deleted in mutation.item_lists_deleted:
                if (
                    self.container.item_list
                    and self.container.item_name == item_list_deleted.item.item_name
                ):
                    return mutation
            for item_deleted in mutation.items_deleted:
                if (
                    self.container.item_list
                    and self.container.item_name == item_deleted.item_name
                ):
                    return mutation
