def get_meta_data_by_fn(_, __):
    return {
        "graphqlClient.ts.j2": {
            "include": bool(_.react_app.use_graphql),
        },
    }
