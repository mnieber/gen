def get_helpers(_):
    class Helpers:
        state_provider = _.component
        state = state_provider.state

        def __init__(self):
            pass

        def other_bvrs(self, container):
            return [bvr for bvr in container.bvrs if not bvr.is_skandha]

    return Helpers()
