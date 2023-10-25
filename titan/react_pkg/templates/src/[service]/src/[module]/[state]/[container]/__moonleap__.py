from moonleap import u0


def get_helpers(_):
    class Helpers:
        @property
        def item_source(self):
            if _.container.display_bvr:
                return _.container.display_bvr.facet_name
            if _.container.store_bvr:
                return _.container.store_bvr.facet_name
            return None

    return Helpers()


def get_meta_data_by_fn(_, __):
    return {
        ".": {
            "name": "..",
        },
        "registerCtr.ts.j2": {
            "name": f"register{u0(_.container.name)}Ctr.ts",
        },
    }


def get_contexts(_):
    return [dict(container=container) for container in _.state.containers]
