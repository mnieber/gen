def get_meta_data_by_fn(_, __):
    return {
        "[init-project.py.j2]": {
            "name": f"init-{_.project.kebab_name}.py.j2",
        },
    }
