def get_item_by_name(self, item_name):
    for item in self.items:
        if item.item_name == item_name:
            return item
    return None


def get_item_list_by_name(self, item_name):
    for item_list in self.item_lists:
        if item_list.item_name == item_name:
            return item_list
    return None
