from moonleap import u0


def get_meta_data_by_fn(_, __):
    return {
        ".": {
            "name": "..",
            "include": bool(_.module.routes),
        },
        "Switch.tsx.j2": {
            "name": f"{u0(_.module.name)}Switch.tsx",
        },
    }
