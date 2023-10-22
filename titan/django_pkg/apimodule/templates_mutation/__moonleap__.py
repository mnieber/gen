from moonleap.utils.fp import append_uniq


def get_helpers(_):
    class Helpers:
        input_field_specs = _.mutation.api_spec.get_inputs()
        optional_input_field_specs = [x for x in input_field_specs if x.is_optional]
        required_input_field_specs = [x for x in input_field_specs if not x.is_optional]
        fk_input_field_specs = _.mutation.api_spec.get_inputs(["fk", "relatedSet"])
        output_field_specs = _.mutation.api_spec.get_outputs()
        fk_output_field_specs = _.mutation.api_spec.get_outputs(["fk", "relatedSet"])

        @property
        def type_specs_to_import(self):
            result = []
            for field_spec in self.fk_input_field_specs + self.fk_output_field_specs:
                if not field_spec.target_type_spec.only_api:
                    append_uniq(result, field_spec.target_type_spec)

            return result

        def graphene_type(self, field_spec):
            return field_spec.graphene_type(
                "" if field_spec.is_optional else "required=True"
            )

    return Helpers()


def get_meta_data_by_fn(_, __):
    return {
        "graphql_mutation.py.j2": {
            "name": f"{_.mutation.name.lower()}.py",
        }
    }
