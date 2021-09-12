from moonleap import chop0
from moonleap.resource.slctrs import PropSelector, Selector
from titan.tools_pkg.makefile.resources import MakefileRule

init_rule_body = chop0(
    """
init:
\techo "TODO: use this rule to run makefile tasks that will initialize the service."
"""
)


def get_makefile_rules():
    slctr = Selector(
        [
            PropSelector(lambda x: x.tools),
            PropSelector(lambda x: x.makefile_rules.merged),
        ]
    )

    def getter(self):
        makefile_rules = list(slctr.select_from(self))
        return sorted(
            makefile_rules + [MakefileRule(name="init", text=init_rule_body)],
            key=lambda x: x.name,
        )

    return getter
