import ramda as R


def queries_that_provide_item(self, item_name):
    return [q for q in self.queries if q.provides_item(item_name)]


def queries_that_provide_item_list(self, item_name):
    return [q for q in self.queries if q.provides_item_list(item_name)]


def types(self):
    result = []
    for endpoint in list(self.queries) + list(self.mutations):
        for field_spec in list(endpoint.inputs_type_spec.field_specs) + list(
            endpoint.outputs_type_spec.field_specs
        ):
            if field_spec.fk_type_spec:
                result.append(field_spec.fk_type_spec.type_name)
    return R.uniq(result)
