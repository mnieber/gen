import moonleap.resource.props as P
import ramda as R
from moonleap import extend, rule, tags
from moonleap.resource.rel import create_forward
from moonleap.resources.data_type_spec_store import data_type_spec_store
from moonleap.verbs import has, posts, provides
from titan.api_pkg.graphqlapi import GraphqlApi

from . import data_types
from .resources import Mutation


@tags(["mutation"])
def create_mutation(term, block):
    mutation = Mutation(name=term.data)
    return mutation


@rule("graphql:api", posts, "item")
def graphql_api_posts_item(graphql_api, item):
    return [create_forward(graphql_api, has, f"post-{item.item_name}:mutation")]


@rule("graphql:api", posts, "item")
def mutation_posts_item(graphql_api, item):
    mutation = R.find(lambda x: x.name == f"post-{item.item_name}")(
        graphql_api.mutations
    )
    data_type = data_type_spec_store.get_spec(item.item_name)
    mutation.data_type_inputs = data_type
    mutation.data_type_output = data_types.mutation_output_data_type
    return [create_forward(mutation, posts, f"{item.item_name}:item", obj_res=item)]


empty_rules = [
    ("graphql:api", has, "mutation"),
    ("mutation", posts, "item"),
]


@extend(GraphqlApi)
class ExtendGraphqlApi:
    mutations = P.children(has, "mutation")


@extend(Mutation)
class ExtendMutation:
    items_posted = P.children(provides, "item")
