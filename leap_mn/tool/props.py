import ramda as R
from moonleap.prop import Prop
from moonleap.slctrs import PropSelector, Selector


def get_package_names(prop_name, is_dev=False):
    fltr = R.filter(lambda x: x.is_dev == is_dev)
    slctr = Selector(
        [
            PropSelector("tools"),
            PropSelector(prop_name, fltr=fltr),
            PropSelector("package_names"),
        ]
    )

    def getter(self):
        return slctr.select_from(self)

    return Prop(getter)


def get_makefile_rules():
    slctr = Selector(
        [
            PropSelector("tools"),
            PropSelector("makefile_rules"),
        ]
    )

    def getter(self):
        return slctr.select_from(self)

    return Prop(getter)
