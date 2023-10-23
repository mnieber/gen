from moonleap import u0


def get_meta_data_by_fn(_, __):
    return {
        "NavPage.tsx.j2": {
            "name": f"{u0(_.nav_page.module.name)}NavPage.tsx",
        },
    }
