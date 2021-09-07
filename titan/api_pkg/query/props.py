def provides_item(self, item_name):
    return [x for x in self.items_provided if x.item_name == item_name]


def provides_item_list(self, item_name):
    return [x for x in self.item_lists_provided if x.item_name == item_name]
