from moonleap import u0


def get_helpers(_):
    class Helpers:
        use_in_client = _.query.api_spec.use_in_client
        input_field_specs = _.query.api_spec.get_inputs()

    return Helpers()


def get_meta_data_by_fn(_, __):
    return {
        "graphql_query.ts.j2": {
            "name": f"use{_.query.name | u0}.ts",
            "include": bool(__.use_in_client),
        },
    }
