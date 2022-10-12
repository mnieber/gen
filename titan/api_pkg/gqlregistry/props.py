from moonleap.utils.queue import Queue


def get_public_items(gql_reg, predicate):
    result = []
    q = Queue(lambda x: x.type_name, [])

    for endpoint in list(gql_reg.mutations) + list(gql_reg.queries):
        q.extend(
            [
                fk_field_spec.target_item
                for fk_field_spec in endpoint.gql_spec.get_inputs(["fk", "relatedSet"])
            ]
        )
        q.extend(
            [
                fk_field_spec.target_item
                for fk_field_spec in endpoint.gql_spec.get_outputs(["fk", "relatedSet"])
            ]
        )

    for item in q:
        result.append(item)
        q.extend(
            [
                field_spec.target_item
                for field_spec in item.type_spec.get_field_specs(["fk", "relatedSet"])
                if predicate(field_spec)
            ]
        )

    return result
