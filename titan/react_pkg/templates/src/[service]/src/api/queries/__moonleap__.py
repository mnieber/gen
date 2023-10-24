from moonleap import u0


def get_helpers(_):
    class Helpers:
        input_field_specs = _.query.api_spec.get_inputs()

    return Helpers()


def get_meta_data_by_fn(_, __):
    return {
        "graphql_query.ts.j2": {
            "name": f"use{u0(_.query.name)}.ts",
        },
    }


def get_contexts(_):
    return [
        dict(query=query)
        for query in sorted(
            _.api_reg.get_queries(module_name="api"), key=lambda x: x.name
        )
        if query.api_spec.use_in_client
    ]
