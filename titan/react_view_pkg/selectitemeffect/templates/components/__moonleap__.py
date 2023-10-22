from moonleap import u0


def get_meta_data_by_fn(_, __):
    return {
        "SelectItemEffect.tsx.j2": {
            "name": f"{u0(_.component.name)}.tsx",
        },
    }
