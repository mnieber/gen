from titan.api_pkg.apiregistry import get_api_reg
from titan.types_pkg.typeregistry import get_type_reg


def get_meta_data_by_fn(_, __):
    return {
        "graphqlClient.ts.j2": {
            "include": bool(_.react_app.use_graphql),
        },
    }


def get_contexts(_):
    return [dict(api_reg=get_api_reg(), type_reg=get_type_reg())]
