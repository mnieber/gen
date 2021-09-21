import ramda as R
from moonleap.resources.type_spec_store import type_spec_store


def queries_that_provide_item(self, item_name):
    return [q for q in self.queries if q.provides_item(item_name)]


def queries_that_provide_item_list(self, item_name):
    return [q for q in self.queries if q.provides_item_list(item_name)]


def form_type_specs(self):
    result = []
    for endpoint in list(self.queries) + list(self.mutations):
        for field_spec in endpoint.inputs_type_spec.field_specs:
            if field_spec.field_type in ("form",):
                fk_type_name = field_spec.fk_type_spec.type_name
                form_type_spec = type_spec_store().get(fk_type_name)
                result.append(form_type_spec)
    return R.uniq(result)


def data_type_specs(self):
    result = []
    for endpoint in list(self.queries) + list(self.mutations):
        for field_spec in endpoint.outputs_type_spec.field_specs:
            if field_spec.field_type in ("fk",):
                fk_type_name = field_spec.fk_type_spec.type_name
                data_type_spec = type_spec_store().get(fk_type_name)
                result.append(data_type_spec)
    return R.uniq(result)
