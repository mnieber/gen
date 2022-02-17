def mutations_that_post_item(self, item_name):
    return [m for m in self.mutations if m.posts_item(item_name)]
