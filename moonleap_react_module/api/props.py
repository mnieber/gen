def provides_item_list(self, item_list):
    return bool([x for x in self.item_lists if x.item_name == item_list.item_name])


def construct_item_list_section(self, item_list):
    return ""


def load_item_list_section(self, item_list):
    return ""


def save_list_item_section(self, item_list):
    return ""
