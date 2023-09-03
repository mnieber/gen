def get_helpers(_):
    class Helpers:
        state = _.state_provider.state

        def __init__(self):
            pass

    return Helpers()
