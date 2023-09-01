from moonleap import append_uniq


def get_helpers(_):
    class Helpers:
        provided_states = list()
        bvr_names = list()
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
                        if not [x for x in data["bvrs"] if x.name == bvr.name]:
                            data["bvrs"].append(bvr)

                for bvr in container.bvrs:
                    append_uniq(self.bvr_names, bvr.name)

    return Helpers()
