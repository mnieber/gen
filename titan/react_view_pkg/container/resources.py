import typing as T
from dataclasses import dataclass

from moonleap import Resource


@dataclass
class Container(Resource):
    name: str

    def get_bvr(self, name):
        for bvr in self.bvrs:
            if bvr.facet_name == name:
                return bvr
        return None

    @property
    def deletion_bvr(self):
        return self.get_bvr("Deletion")

    @property
    def addition_bvr(self):
        return self.get_bvr("Addition")

    @property
    def display_bvr(self):
        return self.get_bvr("Display")

    @property
    def drag_and_drop_bvr(self):
        return self.get_bvr("DragAndDrop")

    @property
    def edit_bvr(self):
        return self.get_bvr("Edit")

    @property
    def filtering_bvr(self):
        return self.get_bvr("Filtering")

    @property
    def highlight_bvr(self):
        return self.get_bvr("Highlight")

    @property
    def insertion_bvr(self):
        return self.get_bvr("Insertion")

    @property
    def pagination_bvr(self):
        return self.get_bvr("Pagination")

    @property
    def store_bvr(self):
        return self.get_bvr("Store")

    @property
    def selection_bvr(self):
        return self.get_bvr("Selection")
