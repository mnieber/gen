def get_meta_data_by_fn(_, __):
    return {
        "bvr.ts.j2": {
            "name": f"{_.bvr.name}.ts",
        },
    }


def get_contexts(_):
    result = []
    for container in _.state.containers:
        for bvr in container.bvrs:
            if not bvr.is_skandha:
                result.append(dict(bvr=bvr))
    return result
