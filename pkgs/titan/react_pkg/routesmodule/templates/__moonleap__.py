def get_helpers(_):
    class Helpers:
        modules_with_routes = []

        def __init__(self):
            self.modules_with_routes = [
                x for x in _.react_app.modules if x.routes or x.name == "auth"
            ]

    return Helpers()
