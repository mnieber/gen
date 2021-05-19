from moonleap import chop0
from moonleap_tools.makefile import MakefileRule


def get():
    return MakefileRule(
        chop0(
            """
runserver:
\tdocker-entrypoint.sh strapi develop
"""
        )
    )
