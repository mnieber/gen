import os
import typing as T
from dataclasses import dataclass, field

import ramda as R
from moonleap import get_session
from moonleap.parser.term import word_to_term
from moonleap.resources.data_type_spec_store import FK, RelatedSet, data_type_spec_store
from moonleap.utils.case import kebab_to_camel, lower0, upper0
from moonleap.utils.inflect import plural

from .endpoint import get_endpoint_mutation_text, get_endpoint_query_text


@dataclass
class Endpoint:
    name: str
    input_args: dict = field(default_factory=dict)
    item_name: T.Optional[str] = None
    is_list: T.Optional[bool] = None


def add_output_to_endpoint(items, item_lists, output_value, endpoint):
    term = word_to_term(output_value)
    if term is None:
        raise Exception(f"Could not parse output value {output_value}")

    item_name = kebab_to_camel(term.data)
    endpoint.item_name = item_name

    if term.tag == "item":
        endpoint.is_list = False
        items.append(item_name)

    if term.tag == "item-list":
        endpoint.is_list = True
        item_lists.append(item_name)


def add_input_args_to_endpoint(input_values, endpoint):
    for input_value in input_values:
        term = word_to_term(input_value)
        if term is None:
            endpoint.input_args[input_value] = "string"
        else:
            endpoint.input_args[f"{input_value.data}_{input_value.tag}"] = upper0(
                kebab_to_camel(term.data)
            )


def get_queries(res):
    queries = []
    items = []
    item_lists = []

    query_dicts = get_session().settings.get("queries", {})
    for endpoint_name, query_dict in query_dicts.items():
        query = Endpoint(name=kebab_to_camel(endpoint_name))
        queries.append(query)
        add_input_args_to_endpoint(query_dict.get("in", []), query)
        add_output_to_endpoint(items, item_lists, query_dict["out"], query)

    for item_loaded in res.items_loaded:
        if item_loaded.item_name not in items:
            query = Endpoint(
                name=f"get{upper0(item_loaded.item_name)}",
                is_list=False,
                item_name=item_loaded.item_name,
            )
            queries.append(query)

    for item_list_loaded in res.item_lists_loaded:
        if item_list_loaded.item_name not in item_lists:
            query = Endpoint(
                name=f"get{upper0(plural(item_list_loaded.item_name))}",
                is_list=True,
                item_name=item_list_loaded.item_name,
            )
            queries.append(query)

    return queries


def get_mutations(res):
    mutations = []
    items = []
    item_lists = []

    mutation_dicts = get_session().settings.get("mutations", {})

    for endpoint_name, mutation_dict in mutation_dicts.items():
        mutation = Endpoint(name=kebab_to_camel(endpoint_name))
        mutations.append(mutation)
        add_output_to_endpoint(items, item_lists, mutation_dict["out"], mutation)
        add_input_args_to_endpoint(mutation_dict.get("in", []), mutation)

    for form_posted in res.forms_posted:
        mutation_name = f"post{upper0(form_posted.name)}"
        if not [m for m in mutations if m.name == mutation_name]:
            mutation = Endpoint(name=mutation_name)
            mutations.append(mutation)

    for item_posted in res.items_posted:
        mutation_name = f"post{upper0(item_posted.item_name)}"
        if not [m for m in mutations if m.name == mutation_name]:
            mutation = Endpoint(name=mutation_name)
            mutations.append(mutation)

    return mutations


def schema_item_names(queries, mutations):
    result = []
    for endpoint in [*queries, *mutations]:
        if endpoint.item_name:
            result.append(endpoint.item_name)
    return R.uniq(result)


class Sections:
    def __init__(self, res):
        self.res = res

    def schemas(self):
        result = []
        queries = get_queries(self.res)
        mutations = get_mutations(self.res)
        item_names = schema_item_names(queries, mutations)

        for item_name in sorted(item_names):
            result.append(
                f"const {item_name} = new schema.Entity('{plural(item_name)}');"
            )
            # TODO item_name
            if [q for q in queries if item_name == q.item_name and q.is_list]:
                result.append(
                    f"const {plural(item_name)} = new schema.Array({item_name});"
                )
        result.append(os.linesep)

        for item_name in sorted(item_names):
            spec = data_type_spec_store.get_spec(item_name)
            for spec_field in spec.fields:
                if isinstance(spec_field.field_type, FK):
                    result.append(
                        f"{item_name}.define({{ {lower0(spec_field.field_type.target)} }});"  # noqa: E501
                    )
                if isinstance(spec_field.field_type, RelatedSet):
                    result.append(
                        f"{item_name}.define({{ {lower0(plural(spec_field.field_type.target))} }});"  # noqa: E501
                    )

        return os.linesep.join(result)

    def queries(self):
        result = []
        queries = get_queries(self.res)

        for query in queries:
            text = get_endpoint_query_text(query)
            result.append(text)

        return os.linesep.join(result)

    def mutations(self):
        result = []
        mutations = get_mutations(self.res)

        for mutation in mutations:
            text = get_endpoint_mutation_text(mutation)
            result.append(text)

        return os.linesep.join(result)
