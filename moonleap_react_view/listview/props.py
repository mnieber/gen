def name(self):
    return self.item_list.name.title() + "ListView"


def item_list(self):
    for item_list in self.module.item_lists:
        if item_list.item_name == self.item_name:
            return item_list
    return None
