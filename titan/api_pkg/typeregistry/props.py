def get_item_type_by_name(self, item_type_name):
    for item_type in self.item_types:
        if item_type.name == item_type_name:
            return item_type
    return None
