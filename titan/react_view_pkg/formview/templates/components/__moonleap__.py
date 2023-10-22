from moonleap import u0


def get_meta_data_by_fn(_, __):
    return {
        "FormView": {
            "name": f"{u0(_.component.name)}",
        },
    }
