def get_meta_data_by_fn(_, __):
    return {
        ".": {
            "include": bool(_.service.is_python),
        },
        "prod.in.j2": {
            "include": bool(_.project.has_prod_config),
        },
    }
