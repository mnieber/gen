from moonleap.utils.fp import append_uniq


def get_helpers(_):
    class Helpers:
        input_field_specs = list(_.query.api_spec.get_inputs())
        output_field_specs = list(_.query.api_spec.get_outputs())
        required_input_field_specs = [x for x in input_field_specs if not x.is_optional]
        optional_input_field_specs = [x for x in input_field_specs if x.is_optional]

        @property
        def type_specs_to_import(self):
            result = []
            for field_spec in _.query.api_spec.get_outputs(["fk", "relatedSet"]):
                if not field_spec.target_type_spec.only_api:
                    append_uniq(result, field_spec.target_type_spec)

            return result

    return Helpers()


def get_meta_data_by_fn(_, __):
    return {
        "graphql_query.py.j2": {
            "name": f"{_.query.name.lower()}.py",
        }
    }


def get_contexts(_):
    return [dict(query=query) for query in _.api_reg.get_queries(module_name="api")]
