import moonleap.resource.props as P
from moonleap import Prop, create, empty_rule, extend, kebab_to_camel
from moonleap.verbs import deletes, has, provides, saves

from . import props
from .resources import Mutation

base_tags = {
    "mutation": ["api-endpoint"],
}


rules = {
    (":gql-registry", has, "mutation"): empty_rule(),
    ("mutation", saves, "item"): empty_rule(),
    ("mutation", deletes, "item~list"): empty_rule(),
    ("mutation", provides, "x+item"): empty_rule(),
    ("mutation", provides, "x+item~list"): empty_rule(),
}


@create("mutation")
def create_mutation(term):
    mutation = Mutation(name=kebab_to_camel(term.data))
    return mutation


@extend(Mutation)
class ExtendMutation:
    items_saved = P.children(saves, "item")
    item_lists_saved = P.children(saves, "item~list")
    items_deleted = P.children(deletes, "item")
    item_lists_deleted = P.children(deletes, "item~list")
    gql_spec = Prop(props.gql_spec)
