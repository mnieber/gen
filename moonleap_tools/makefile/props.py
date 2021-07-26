from moonleap.resource.slctrs import PropSelector, Selector


def get_makefile_rules():
    slctr = Selector(
        [
            PropSelector(lambda x: x.tools),
            PropSelector(lambda x: x.makefile_rules.merged),
        ]
    )

    def getter(self):
        return slctr.select_from(self)

    return getter
