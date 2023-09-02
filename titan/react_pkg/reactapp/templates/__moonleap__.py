from moonleap import append_uniq, u0
from moonleap.utils.inflect import plural


def get_helpers(_):
    class Helpers:
        provided_states = list()
        bvrs = list()
        skandha_bvrs = list()
        item_names = list()
        provided_data = dict()

        def __init__(self):
            for module in _.react_app.modules:
                for component in module.components:
                    if component.meta.term.tag == "state~provider":
                        state = component.state
                        self._add_state(state)

        def _add_state(self, state):
            self.provided_states.append(state)
            for container in state.containers:
                if container.item_list:
                    append_uniq(self.item_names, container.item_list.item_name)
                    data = self.provided_data.setdefault(
                        container.item_list.item_name, {}
                    )
                    data["item_list"] = container.item_list
                    if container.get_bvr("highlight"):
                        data["item"] = container.item_list.item
                    data["bvrs"] = data.setdefault("bvrs", [])
                    for bvr in container.bvrs:
                        if _is_exposed_bvr(bvr):
                            if not [x for x in data["bvrs"] if x.name == bvr.name]:
                                data["bvrs"].append(bvr)

                for bvr in container.bvrs:
                    if _is_exposed_bvr(bvr):
                        append_uniq(self.bvrs, bvr)
                        if bvr.is_skandha:
                            append_uniq(self.skandha_bvrs, bvr)

        def section_names(self):
            result = ["dpsStates"]
            for key in self.provided_data.keys():
                result.append(f"dps{ u0(plural(key)) }")
            return sorted(result)

    return Helpers()


def _is_exposed_bvr(bvr):
    return bvr.facet_name not in ("store", "display")
