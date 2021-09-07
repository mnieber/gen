def queries_that_provide_item(self, item_name):
    return [q for q in self.queries if q.provides_item(item_name)]


def queries_that_provide_item_list(self, item_name):
    return [q for q in self.queries if q.provides_item_list(item_name)]


def mutations_that_post_item(self, item_name):
    return [m for m in self.mutations if m.posts_item(item_name)]


def item_types(self):
    result = []
    for query in self.queries:
        for item in query.items_provided:
            if item.item_type not in result:
                result.append(item.item_type)
        for item_list in query.item_lists_provided:
            if item_list.item_type not in result:
                result.append(item_list.item_type)

    for mutation in self.mutations:
        for item in mutation.items_posted:
            if item.item_type not in result:
                result.append(item.item_type)

    return result
