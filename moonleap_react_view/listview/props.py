from moonleap.utils import title


def name(self):
    return title(self.item_list.name) + "ListView"


def item_list(self):
    for item_list in self.module.item_lists:
        if item_list.item_name == self.item_name:
            return item_list
    return None
