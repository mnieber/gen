def get_helpers(_):
    class Helpers:
        states = []

        def __init__(self):
            for module in _.react_app.modules:
                for state in module.states:
                    self.states.append(state)

    return Helpers()
