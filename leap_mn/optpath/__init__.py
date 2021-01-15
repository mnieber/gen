import moonleap.props as P

from .resources import OptPath


class StoreOptPaths:
    opt_paths = P.tree(
        "has", "opt-path", merge=lambda acc, x: [*acc, x], initial=list()
    )
