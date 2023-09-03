import typing as T
from dataclasses import dataclass, field

from moonleap import Resource, named
from titan.react_view_pkg.behavior import Behavior
from titan.types_pkg.itemlist import ItemList


@dataclass
class Container(Resource):
    name: str

    def get_bvr(self, name):
        for bvr in self.bvrs:
            if bvr.facet_name == name:
                return bvr
        return None

    @property
    def store_bvr(self):
        return self.get_bvr("store")

    @property
    def deletion_bvr(self):
        return self.get_bvr("deletion")

    @property
    def display_bvr(self):
        return self.get_bvr("display")

    @property
    def edit_bvr(self):
        return self.get_bvr("edit")

    @property
    def drag_and_drop_bvr(self):
        return self.get_bvr("dragAndDrop")
