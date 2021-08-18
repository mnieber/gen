from moonleap import chop0
from titan.tools_pkg.makefile import MakefileRule


def get_runserver():
    return MakefileRule(
        name="runserver",
        text=chop0(
            """
runserver:
\tyarn start
"""  # noqa
        ),
    )


def get_install():
    return MakefileRule(
        name="install",
        text=chop0(
            """
install:
\tyarn install
"""  # noqa
        ),
    )
