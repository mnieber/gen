def get_meta_data_by_fn(_, __):
    return {
        ".": {
            "include": bool(_.service.api_module),
        }
    }

