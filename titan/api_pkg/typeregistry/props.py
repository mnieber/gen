def get_item_by_name(self, item_name):
    for item in self.items:
        if item.item_name == item_name:
            return item
    return None
