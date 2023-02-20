from dataclasses import dataclass, field

from moonleap import named
from titan.react_pkg.component.resources import Component
from titan.react_view_pkg.behavior import Behavior
from titan.types_pkg.itemlist import ItemList


@dataclass
class State(Component):
    containers: list["Container"] = field(default_factory=list)


@dataclass
class UrlState(State):
    pass


@dataclass
class Container:
    name: str
    bvrs: list[Behavior] = field(default_factory=list)
    named_item_list: named(ItemList) = None
    named_items: list[named(ItemList)] = field(default_factory=list)

    def get_bvr(self, name):
        for bvr in self.bvrs:
            if bvr.name == name:
                return bvr
        return None

    @property
    def item(self):
        if self.named_item_list:
            return self.named_item_list.typ.item
        return None

    @property
    def deletion_bvr(self):
        return self.get_bvr("deletion")

    @property
    def editing_bvr(self):
        return self.get_bvr("editing")

    @property
    def drag_and_drop_bvr(self):
        return self.get_bvr("dragAndDrop")

    @property
    def delete_items_mutation(self):
        if bvr := self.deletion_bvr:
            mutation = bvr.mutation
            item_names = (
                [x.item.item_name for x in mutation.item_lists_deleted]
                if mutation
                else []
            )
            if bvr.item_name in item_names:
                return mutation
        return None

    @property
    def delete_item_mutation(self):
        if bvr := self.deletion_bvr:
            mutation = bvr.mutation
            item_names = (
                [x.item_name for x in mutation.items_deleted] if mutation else []
            )
            if bvr.item_name in item_names:
                return mutation
        return None

    @property
    def order_items_mutation(self):
        if bvr := self.get_bvr("insertion"):
            return bvr.mutation
        return None

    @property
    def save_item_mutation(self):
        if bvr := self.get_bvr("editing"):
            return bvr.mutation
        return None
