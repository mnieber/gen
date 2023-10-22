def get_meta_data_by_fn(_, __):
    return {
        "StateProvider.tsx.j2": {
            "name": f"{_.component.name}.tsx",
        },
    }
