import moonleap.resource.props as P
from moonleap import MemFun, create, create_forward, empty_rule, extend, rule
from moonleap.session import get_session
from moonleap.utils.case import camel_to_kebab, l0
from moonleap.verbs import deletes, has, provides, saves
from titan.api_pkg.pkg.load_api_specs import load_api_specs

from . import props
from .resources import ApiRegistry

rules = {
    ("project", has, ":api-registry"): empty_rule(),
    ("api-registry", has, "api-endpoint"): empty_rule(),
    ("api-registry", has, "mutation"): empty_rule(),
    ("api-registry", has, "query"): empty_rule(),
    ("project", has, "api-registry"): empty_rule(),
}

_api_registry = None


def get_api_reg():
    global _api_registry
    if not _api_registry:
        _api_registry = ApiRegistry()
        load_api_specs(_api_registry, get_session().spec_dir)

    return _api_registry


@create("api-registry")
def create_api_registry(term):
    global _api_registry
    if _api_registry:
        raise Exception("The api registry should be created only once")
    return get_api_reg()


@rule("project")
def created_project(project):
    return create_forward(project, has, ":api-registry")


@rule("api-registry")
def created_api_registry(api_reg):
    forwards = []
    for api_spec in get_api_reg().api_specs():
        tag = "mutation" if api_spec.is_mutation else "query"
        endpoint_term = camel_to_kebab(l0(api_spec.name)) + ":" + tag
        forwards.append(create_forward(api_reg, has, endpoint_term))

        for field_spec in api_spec.get_outputs(["fk", "relatedSet"]):
            term = (
                "+"
                + camel_to_kebab(l0(field_spec.target))
                + ":item"
                + ("~list" if field_spec.field_type == "relatedSet" else "")
            )
            forwards.append(create_forward(endpoint_term, provides, term))

        for type_name_deleted, is_list in api_spec.deletes:
            term = (
                camel_to_kebab(l0(type_name_deleted))
                + ":item"
                + ("~list" if is_list else "")
            )
            forwards.append(create_forward(endpoint_term, deletes, term))

        for type_name_saved, is_list in api_spec.saves:
            term = (
                camel_to_kebab(l0(type_name_saved))
                + ":item"
                + ("~list" if is_list else "")
            )
            forwards.append(create_forward(endpoint_term, saves, term))

    return forwards


@extend(ApiRegistry)
class ExtendApiRegistry:
    mutations = P.children(has, "mutation")
    queries = P.children(has, "query")
    get_public_items = MemFun(props.get_public_items)
    get_form_type_specs = MemFun(props.get_form_type_specs)
