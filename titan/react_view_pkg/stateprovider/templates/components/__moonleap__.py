def get_helpers(_):
    class Helpers:
        state = _.component.state
        pipelines = _.component.pipelines

        input_items = list()
        input_item_lists = list()
        queries = list()
        mutations = list()

        def __init__(self):
            pass

    return Helpers()
