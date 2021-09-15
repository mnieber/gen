def queries_that_provide_item(self, item_name):
    return [q for q in self.queries if q.provides_item(item_name)]


def queries_that_provide_item_list(self, item_name):
    return [q for q in self.queries if q.provides_item_list(item_name)]


def types(self):
    result = []
    for endpoint in list(self.queries) + list(self.mutations):
        for field_spec in list(
            endpoint.inputs_type_spec.field_spec_by_name.values()
        ) + list(endpoint.outputs_type_spec.field_spec_by_name.values()):
            if field_spec.field_type in ("fk", "list"):
                result.append(field_spec.field_type_attrs["target"])
    return result
