def get_meta_data_by_fn(_, __):
    return {
        "KeyHandler.tsx.j2": {
            "name": f"{__.component_name}.tsx",
        },
    }
