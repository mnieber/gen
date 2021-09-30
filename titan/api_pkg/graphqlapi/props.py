def mutations_that_post_item(self, item_name):
    return [m for m in self.mutations if m.posts_item(item_name)]


def item_types(self):
    result = []

    def add_items(items):
        for item in items:
            if item.item_type not in result:
                result.append(item.item_type)
                add_items([x for x in item.items_provided])
                add_items([x.item for x in item.item_lists_provided])

    for query in self.queries:
        add_items([x for x in query.items_provided])
        add_items([x.item for x in query.item_lists_provided])

    for mutation in self.mutations:
        add_items([x for x in mutation.items_posted])

    return result
