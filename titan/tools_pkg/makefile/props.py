from moonleap import chop0
from titan.tools_pkg.makefile.resources import MakefileRule

init_rule_body = chop0(
    """
init:
\techo "TODO: use this rule to run makefile tasks that will initialize the service."
"""
)


def get_makefile_rules():
    def getter(self):
        makefile_rules = []
        for tool in self.tools:
            makefile_rules.extend(tool.makefile_rules.merged)

        return sorted(
            makefile_rules + [MakefileRule(name="init", text=init_rule_body)],
            key=lambda x: x.name,
        )

    return getter
