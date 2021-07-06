import ramda as R


def item_names(self):
    return R.uniq(
        [x.item_name for x in self.items] + [x.item_name for x in self.item_lists]
    )
