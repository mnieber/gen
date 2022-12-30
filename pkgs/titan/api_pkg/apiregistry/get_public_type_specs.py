from moonleap.utils.fp import append_uniq
from moonleap.utils.queue import Queue
from titan.types_pkg.typeregistry import get_type_reg


def get_public_type_specs(api_reg, include_stubs, predicate):
    type_reg = get_type_reg()
    result = []
    q = Queue(lambda x: x.type_name, [])

    for endpoint in list(api_reg.mutations) + list(api_reg.queries):
        if not include_stubs and endpoint.api_spec.is_stub:
            continue
        _add_target_type_specs(q, endpoint.api_spec.get_inputs(["fk", "relatedSet"]))
        _add_target_type_specs(q, endpoint.api_spec.get_outputs(["fk", "relatedSet"]))

    for type_spec in q:
        append_uniq(result, type_spec)
        if type_spec.base_type_name:
            append_uniq(result, type_reg.get(type_spec.base_type_name))
        _add_target_type_specs(
            q, type_spec.get_field_specs(["fk", "relatedSet"]), predicate
        )

    return result


def _add_target_type_specs(q, field_specs, predicate=None):
    q.extend(
        [
            field_spec.target_type_spec
            for field_spec in field_specs
            if (not predicate or predicate(field_spec))
        ]
    )
