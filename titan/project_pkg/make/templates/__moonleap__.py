def get_meta_data_by_fn(_, __):
    return {
        "Makefile.prod.j2": {
            "include": bool(_.project.has_prod_config),
        },
    }
