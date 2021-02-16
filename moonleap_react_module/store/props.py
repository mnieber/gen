import os


def policy_lines(store):
    result = []
    return os.linesep.join(result)


def item_names(store):
    return [x.item_name for x in store.item_lists]
