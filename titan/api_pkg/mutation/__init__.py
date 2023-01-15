from titan.api_pkg.apiregistry.resources import Mutation  # noqa

from moonleap import create, kebab_to_camel

base_tags = {
    "mutation": ["api-endpoint"],
}


@create("mutation")
def create_mutation(term):
    from titan.api_pkg.apiregistry import get_api_reg

    mutation_name = kebab_to_camel(term.data)
    return get_api_reg().get_mutation(mutation_name)
