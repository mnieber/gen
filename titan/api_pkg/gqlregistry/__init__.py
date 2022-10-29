import moonleap.resource.props as P
from moonleap import MemFun, create, create_forward, empty_rule, extend, rule
from moonleap.session import get_session
from moonleap.utils.case import camel_to_kebab, l0
from moonleap.verbs import deletes, has, provides, saves

from . import props
from .load_gql_specs import load_gql_specs
from .resources import GqlRegistry

rules = {
    ("project", has, ":gql-registry"): empty_rule(),
    ("gql-registry", has, "api-endpoint"): empty_rule(),
    ("gql-registry", has, "mutation"): empty_rule(),
    ("gql-registry", has, "query"): empty_rule(),
    ("project", has, "gql-registry"): empty_rule(),
}

_gql_registry = None


def get_gql_reg():
    global _gql_registry
    if not _gql_registry:
        _gql_registry = GqlRegistry()
        load_gql_specs(_gql_registry, get_session().spec_dir)

    return _gql_registry


@create("gql-registry")
def create_gql_registry(term):
    global _gql_registry
    if _gql_registry:
        raise Exception("The gql registry should be created only once")
    return get_gql_reg()


@rule("project")
def created_project(project):
    return create_forward(project, has, ":gql-registry")


@rule("gql-registry")
def created_gql_registry(gql_reg):
    forwards = []
    for gql_spec in get_gql_reg().gql_specs():
        tag = "mutation" if gql_spec.is_mutation else "query"
        endpoint_term = camel_to_kebab(l0(gql_spec.name)) + ":" + tag
        forwards.append(create_forward(gql_reg, has, endpoint_term))

        for field_spec in gql_spec.get_outputs(["fk", "relatedSet"]):
            item_term = (
                "+"
                + camel_to_kebab(l0(field_spec.target))
                + ":item"
                + ("~list" if field_spec.field_type == "relatedSet" else "")
            )
            forwards.append(create_forward(endpoint_term, provides, item_term))

        for type_name_deleted, is_list in gql_spec.deletes:
            item_term = (
                camel_to_kebab(l0(type_name_deleted))
                + ":item"
                + ("~list" if is_list else "")
            )
            forwards.append(create_forward(endpoint_term, deletes, item_term))

        for type_name_saved, is_list in gql_spec.saves:
            item_term = (
                camel_to_kebab(l0(type_name_saved))
                + ":item"
                + ("~list" if is_list else "")
            )
            forwards.append(create_forward(endpoint_term, saves, item_term))

    return forwards


@extend(GqlRegistry)
class ExtendGqlReg:
    mutations = P.children(has, "mutation")
    queries = P.children(has, "query")
    get_public_items = MemFun(props.get_public_items)
    get_form_type_specs = MemFun(props.get_form_type_specs)
