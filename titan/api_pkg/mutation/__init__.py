import moonleap.resource.props as P
import ramda as R
from moonleap import MemFun, Prop, create, empty_rule, extend, kebab_to_camel, rule
from moonleap.resource.forward import create_forward
from moonleap.verbs import deletes, has, posts
from titan.api_pkg.graphqlapi import GraphqlApi

from . import props
from .resources import Mutation


@create("mutation", [])
def create_mutation(term, block):
    mutation = Mutation(name=kebab_to_camel(term.data))
    return mutation


@rule("graphql:api", posts, "item")
def graphql_api_posts_item(graphql_api, item):
    mutation_term_str = f"post-{item.item_name}:mutation"
    item_type_term_str = f"{item._meta.term.data}:item~type"
    return [
        create_forward(item_type_term_str, has, f"{item.item_name}:item~form-type"),
        create_forward(graphql_api, has, mutation_term_str),
        create_forward(mutation_term_str, posts, f"{item.item_name}:item"),
    ]


@rule("graphql:api", deletes, "item")
def graphql_api_deletes_item(graphql_api, item):
    mutation_term_str = f"delete-{item.item_name}:mutation"
    return [
        create_forward(graphql_api, has, mutation_term_str),
        create_forward(mutation_term_str, deletes, f"{item.item_name}:item"),
    ]


rules = [
    (("graphql:api", has, "mutation"), empty_rule()),
    (("mutation", posts, "item"), empty_rule()),
]


@extend(GraphqlApi)
class ExtendGraphqlApi:
    mutations = P.children(has, "mutation")


@extend(Mutation)
class ExtendMutation:
    items_deleted = P.children(deletes, "item")
    items_posted = P.children(posts, "item")
    posts_item = MemFun(props.posts_item)
    inputs_type_spec = Prop(props.inputs_type_spec)
    outputs_type_spec = Prop(props.outputs_type_spec)
