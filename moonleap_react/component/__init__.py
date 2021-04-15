from moonleap import extend

from .resources import Component  # noqa


@extend(Component)
class ExtendComponent:
    pass
