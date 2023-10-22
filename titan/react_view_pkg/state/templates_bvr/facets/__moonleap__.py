def get_meta_data_by_fn(_, __):
    return {
        "bvr.ts.j2": {
            "name": f"{_.bvr.name}.ts",
        },
    }
