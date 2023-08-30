def get_helpers(_):
    class Helpers:
        state_provider = _.component
        state = state_provider.state

        def __init__(self):
            pass

    return Helpers()
