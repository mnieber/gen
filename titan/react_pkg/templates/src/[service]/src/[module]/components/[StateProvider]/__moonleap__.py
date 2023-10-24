from titan.react_pkg.behavior.resources import is_exposed_bvr


def get_helpers(_):
    class Helpers:
        state_provider = _.component
        state = state_provider.state

        def __init__(self):
            pass

        def other_bvrs(self, container):
            return [
                bvr
                for bvr in container.bvrs
                if not bvr.is_skandha
                and is_exposed_bvr(bvr)
                and (
                    bvr.facet_name
                    not in [
                        "Addition",
                        "Deletion",
                        "DragAndDrop",
                        "Edit",
                        "Filtering",
                        "Highlight",
                        "Hovering",
                        "Pagination",
                        "Selection",
                    ]
                )
            ]

    return Helpers()


def get_meta_data_by_fn(_, __):
    return {
        "StateProvider.tsx.j2": {
            "name": f"{_.component.name}.tsx",
        },
    }


def get_contexts(_):
    return [
        dict(component=component)
        for component in _.module.components
        if component.meta.term.tag == "state-provider"
    ]
