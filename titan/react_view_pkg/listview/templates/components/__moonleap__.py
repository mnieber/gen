from moonleap import u0


def get_meta_data_by_fn(_, __):
    return {
        "ListView.tsx.j2": {
            "name": f"{u0(_.component.name)}.tsx",
        },
        "ListView.scss.j2": {
            "name": f"{u0(_.component.name)}.scss",
        },
        "ListViewItem.tsx.j2": {
            "name": f"{u0(_.component.name)}Item.tsx",
        },
        "ListViewItem.scss.j2": {
            "name": f"{u0(_.component.name)}Item.scss",
        },
    }
