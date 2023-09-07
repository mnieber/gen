def get_helpers(_):
    class Helpers:
        view = _.component
        item_name = view.item.item_name

        def __init__(self):
            pass

    return Helpers()
