def get_bvr(self, name):
    for bvr in self.bvrs:
        if bvr.name == name:
            return bvr
    return None


def container_item(self):
    if self.named_item_list:
        return self.named_item_list.typ.item
    return None
