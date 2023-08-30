from moonleap import append_uniq


def get_helpers(_):
    class Helpers:
        state = _.state_provider.state
        mutations = []

        def __init__(self):
            self.mutations = self._get_mutations()
            self.type_specs_to_import = self._type_specs_to_import()

        def _get_mutations(self):
            mutations = []
            for container in self.state.containers:
                if delete_items_mutation := container.delete_items_mutation:
                    append_uniq(mutations, delete_items_mutation)
                if delete_item_mutation := container.delete_item_mutation:
                    append_uniq(mutations, delete_item_mutation)
                if save_item_mutation := container.save_item_mutation:
                    append_uniq(mutations, save_item_mutation)
                if order_items_mutation := container.order_items_mutation:
                    append_uniq(mutations, order_items_mutation)
            return mutations

        def _type_specs_to_import(self):
            types = []
            for mutation in self.mutations:
                for field in mutation.api_spec.get_inputs(
                    ["fk", "relatedSet", "uuid", "uuid[]"]
                ):
                    append_uniq(types, field.target_type_spec)
            return types

    return Helpers()
