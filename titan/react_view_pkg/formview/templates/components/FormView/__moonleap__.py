from moonleap import u0


def get_meta_data_by_fn(_, __):
    return {
        "FormView.tsx.j2": {
            "name": f"{u0(_.component.name)}.tsx",
        },
        "FormView.scss.j2": {
            "name": f"{u0(_.component.name)}.scss",
        },
    }
