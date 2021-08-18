from moonleap.resource.slctrs import PropSelector, Selector


def get_makefile_rules():
    slctr = Selector(
        [
            PropSelector(lambda x: x.tools),
            PropSelector(lambda x: x.makefile_rules.merged),
        ]
    )

    def getter(self):
        return sorted(slctr.select_from(self), key=lambda x: x.name)

    return getter
