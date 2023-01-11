from titan.api_pkg.apiregistry.resources import Query  # noqa

from moonleap import create, kebab_to_camel

base_tags = {
    "query": ["api-endpoint"],
}


@create("query")
def create_query(term):
    from titan.api_pkg.apiregistry import get_api_reg

    query_name = kebab_to_camel(term.data)
    return get_api_reg().get_query(query_name)
