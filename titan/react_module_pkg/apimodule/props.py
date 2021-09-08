import os

import ramda as R
from moonleap.resources.type_spec_store import type_spec_store
from moonleap.utils.case import lower0
from moonleap.utils.inflect import plural

from .endpoint import get_endpoint_mutation_text, get_endpoint_query_text


class Sections:
    def __init__(self, res):
        self.res = res
        self.graphql_api = res.graphql_api

    def schemas(self):
        result = []
        item_schemas = set()
        item_list_schemas = set()

        for query in self.graphql_api.queries:
            for item in query.items_provided:
                item_schemas.add(item.item_name)
            for item in query.item_lists_provided:
                item_list_schemas.add(item.item_name)
        item_names = sorted(R.uniq(list(item_schemas) + list(item_list_schemas)))

        for item_name in item_names:
            if item_name in item_schemas:
                result.append(
                    f"const {item_name} = new schema.Entity('{plural(item_name)}');"
                )
            if item_name in item_list_schemas:
                result.append(
                    f"const {plural(item_name)} = new schema.Array({item_name});"
                )

        result.append(os.linesep)

        for item_name in item_names:
            type_spec = type_spec_store.get(item_name)
            for field_spec in type_spec.field_spec_by_name.values():
                if field_spec.field_type == "fk":
                    target = field_spec.field_type_attrs["target"]
                    result.append(
                        f"{item_name}.define({{ {lower0(target)} }});"  # noqa: E501
                    )
                if field_spec.field_type == "related_set":
                    target = field_spec.field_type_attrs["target"]
                    result.append(
                        f"{item_name}.define({{ {lower0(plural(target))} }});"  # noqa: E501
                    )

        return os.linesep.join(result)

    def queries(self):
        result = []

        for query in self.graphql_api.queries:
            text = get_endpoint_query_text(query)
            result.append(text)

        return os.linesep.join(result)

    def mutations(self):
        result = []

        for mutation in self.graphql_api.mutations:
            text = get_endpoint_mutation_text(mutation)
            result.append(text)

        return os.linesep.join(result)
