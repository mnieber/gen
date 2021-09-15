import moonleap.resource.props as P
import ramda as R
from moonleap import MemFun, Prop, create, extend, kebab_to_camel, rule, upper0
from moonleap.resource.rel import create_forward
from moonleap.verbs import deletes, has, posts
from titan.api_pkg.graphqlapi import GraphqlApi

from . import props
from .resources import Mutation


@create(["mutation"])
def create_mutation(term, block):
    mutation = Mutation(name=kebab_to_camel(term.data))
    return mutation


@rule("graphql:api", posts, "item")
def graphql_api_posts_item(graphql_api, item):
    return [create_forward(graphql_api, has, f"post-{item.item_name}:mutation")]


@rule("graphql:api", posts, "item")
def mutation_posts_item(graphql_api, item):
    query_name = f"post{kebab_to_camel(upper0(item.item_name))}"
    mutation = R.find(lambda x: x.name == query_name)(graphql_api.mutations)
    return [create_forward(mutation, posts, f"{item.item_name}:item", obj_res=item)]


@rule("graphql:api", deletes, "item")
def graphql_api_deletes_item(graphql_api, item):
    return [create_forward(graphql_api, has, f"delete-{item.item_name}:mutation")]


@rule("graphql:api", deletes, "item")
def mutation_deletes_item(graphql_api, item):
    query_name = f"delete{kebab_to_camel(upper0(item.item_name))}"
    mutation = R.find(lambda x: x.name == query_name)(graphql_api.mutations)
    return [create_forward(mutation, deletes, f"{item.item_name}:item", obj_res=item)]


empty_rules = [
    ("graphql:api", has, "mutation"),
    ("mutation", posts, "item"),
]


@extend(GraphqlApi)
class ExtendGraphqlApi:
    mutations = P.children(has, "mutation")


@extend(Mutation)
class ExtendMutation:
    items_deleted = P.children(deletes, "item")
    items_posted = P.children(posts, "item")
    inputs_type_spec = Prop(props.inputs_type_spec)
    outputs_type_spec = Prop(props.outputs_type_spec)
