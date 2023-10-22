from moonleap import u0


def get_helpers(_):
    class Helpers:
        use_in_client = _.mutation.api_spec.use_in_client
        input_field_specs = _.mutation.api_spec.get_inputs()
        form_input_field_specs = _.mutation.api_spec.get_inputs(["form"])

        @property
        def form_input_type_specs(self):
            result = []
            for field_spec in self.form_input_field_specs:
                result.append(field_spec.target_type_spec)
            return result

        def split_query_names(self, query_names):
            return [x.split(".") if "." in x else ("api", x) for x in query_names]

        @property
        def orders_field(self):
            return ", ".join([".".join(x) for x in _.mutation.api_spec.orders])

    return Helpers()


def get_meta_data_by_fn(_, __):
    return {
        "graphql_mutation.ts.j2": {
            "name": f"use{_.mutation.name | u0}.ts",
            "include": bool(__.use_in_client),
        },
    }
