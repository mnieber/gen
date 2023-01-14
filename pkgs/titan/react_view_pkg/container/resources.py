from dataclasses import dataclass

from moonleap import Resource


@dataclass
class Container(Resource):
    name: str

    @property
    def delete_items_mutation(self):
        if bvr := self.get_bvr("deletion"):
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
        if bvr := self.get_bvr("deletion"):
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
