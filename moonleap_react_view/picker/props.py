def item_type(self):
    store = self.module.store
    item_types = [x for x in store.item_types if x.name == self.item_type_name]
    return item_types[0] if item_types else None
