from moonleap import u0


def get_meta_data_by_fn(_, __):
    return {
        "NavPage.tsx.j2": {
            "name": f"{u0(_.module.name)}NavPage.tsx",
        },
    }


def get_contexts(_):
    return [dict(module=module) for module in _.react_app.modules if module.nav_page]
