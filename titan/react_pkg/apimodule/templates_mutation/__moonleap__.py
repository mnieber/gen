from titan.react_pkg.apimodule.graphql_body import graphql_body
from titan.types_pkg.pkg.get_paths_to import get_paths_to
from titan.types_pkg.pkg.has_hydrated_fields import has_hydrated_fields
from titan.types_pkg.typeregistry import get_type_reg


def get_helpers(_):
    class Helpers:
        input_field_specs = _.mutation.api_spec.get_inputs()
        form_input_field_specs = _.mutation.api_spec.get_inputs(["form"])
        fk_output_field_specs = _.mutation.api_spec.get_outputs(["relatedSet", "fk"])
        orders_data = []
        hydrated_fields = []

        def __init__(self):
            self.hydrated_fields = self.get_hydrated_fields()
            self.type_specs_to_import, self.graphql_body = graphql_body(
                _.mutation.api_spec.outputs_type_spec, indent=8
            )
            self.set_orders_data()

        @property
        def form_input_type_specs(self):
            result = []
            for field_spec in self.form_input_field_specs:
                result.append(field_spec.target_type_spec)
            return result

        def get_hydrated_fields(self):
            result = []
            for field_spec in self.fk_output_field_specs:
                if has_hydrated_fields(field_spec.target_type_spec, "client"):
                    result.append(field_spec)
            return result

        def set_orders_data(self):
            self.orders_data = []
            for order_parent, order_child in _.mutation.api_spec.orders:
                type_spec = get_type_reg().get(order_parent)
                assert type_spec

                field_spec = type_spec.get_field_spec_by_key(order_child)
                assert field_spec

                order_ids = None
                for input in _.mutation.api_spec.get_inputs(["uuid[]"]):
                    if input.target == field_spec.target:
                        order_ids = input.key

                api_specs = []
                for api_spec in _.api_reg.api_specs():
                    paths = get_paths_to(
                        type_spec.type_name,
                        api_spec,
                        base_path="",
                    )
                    if paths:
                        api_specs.append((api_spec, paths))

                self.orders_data.append(
                    (order_parent, order_child, order_ids, api_specs)
                )

    return Helpers()
