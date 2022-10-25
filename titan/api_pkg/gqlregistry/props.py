from moonleap.utils.fp import append_uniq
from moonleap.utils.queue import Queue


def _add_target_items(q, field_specs, predicate=None):
    q.extend(
        [
            field_spec.target_item
            for field_spec in field_specs
            if (not predicate or predicate(field_spec))
        ]
    )


def get_public_items(gql_reg, predicate):
    result = []
    q = Queue(lambda x: x.type_name, [])

    for endpoint in list(gql_reg.mutations) + list(gql_reg.queries):
        _add_target_items(q, endpoint.gql_spec.get_inputs(["fk", "relatedSet"]))
        _add_target_items(q, endpoint.gql_spec.get_outputs(["fk", "relatedSet"]))

    for item in q:
        result.append(item)
        _add_target_items(
            q, item.type_spec.get_field_specs(["fk", "relatedSet"]), predicate
        )

    return result


def get_form_type_specs(gql_reg):
    result = []

    for mutation in gql_reg.mutations:
        for field_spec in mutation.gql_spec.get_inputs(["form"]):
            append_uniq(result, field_spec.target_type_spec)

    for query in gql_reg.queries:
        for field_spec in query.gql_spec.get_inputs(["form"]):
            append_uniq(result, field_spec.target_type_spec)

    return result
