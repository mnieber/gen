import typing as T
from dataclasses import dataclass, field

from moonleap.utils.fp import append_uniq
from titan.react_view_pkg.behavior import Behavior
from titan.types_pkg.item import Item
from titan.types_pkg.itemlist import ItemList
from titan.types_pkg.typeregistry import get_type_reg


@dataclass
class ProvidedData:
    item: T.Optional[Item] = None
    item_list: T.Optional[ItemList] = None
    bvrs: T.List[Behavior] = field(default_factory=list)


def get_helpers(_):
    class Helpers:
        states = list()
        bvr_names = list()
        item_names = list()
        _provided_data_by_item_name = dict()

        def __init__(self):
            for module in _.react_app.modules:
                for state in module.states:
                    self.states.append(state)

            for module in _.react_app.modules:
                for component in module.components:
                    if component.meta.term.tag == "state~provider":
                        state_provider = component
                        for named_item in state_provider.named_items_provided:
                            self._add_provided_item(named_item)
                        for named_item_list in state_provider.named_item_lists_provided:
                            self._add_provided_item(named_item_list)
                        if state_provider.state:
                            for container in state_provider.state.containers:
                                for named_item in container.named_items:
                                    self._add_provided_item(named_item)
                                self._add_provided_item_list(container.named_item_list)
                                for bvr in container.bvrs:
                                    self._add_provided_bvr(bvr)

        def _add_provided_item(self, named_item):
            if named_item:
                provided_data = self._provided_data_by_item_name.setdefault(
                    named_item.typ.item_name, ProvidedData()
                )
                provided_data.item = named_item.typ
                append_uniq(self.item_names, named_item.typ.item_name)

        def _add_provided_item_list(self, named_item_list):
            if named_item_list:
                provided_data = self._provided_data_by_item_name.setdefault(
                    named_item_list.typ.item_name, ProvidedData()
                )
                provided_data.item_list = named_item_list.typ
                append_uniq(self.item_names, named_item_list.typ.item_name)

        def _add_provided_bvr(self, bvr):
            provided_data = self._provided_data_by_item_name.setdefault(
                bvr.item_name, ProvidedData()
            )
            append_uniq(provided_data.bvrs, bvr)
            append_uniq(self.bvr_names, bvr.name)

            if bvr.name == "highlight":
                provided_data.item = get_type_reg().get_item(bvr.item_name)
                append_uniq(self.item_names, bvr.item_name)

        @property
        def provided_data(self):
            return sorted(self._provided_data_by_item_name.items(), key=lambda x: x[0])

    return Helpers()
