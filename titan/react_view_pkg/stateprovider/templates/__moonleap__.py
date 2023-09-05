from titan.react_view_pkg.behavior.resources import is_exposed_bvr


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
