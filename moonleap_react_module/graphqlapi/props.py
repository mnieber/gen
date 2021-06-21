def provides_item_list(self, item_list):
    return bool([x for x in self.item_lists if x.item_name == item_list.item_name])
