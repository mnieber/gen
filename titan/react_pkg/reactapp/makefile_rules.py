from moonleap import chop0
from titan.tools_pkg.makefile import MakefileRule


def get():
    return MakefileRule(
        chop0(
            """
runserver:
\tyarn start

install:
\tyarn install

"""  # noqa
        )
    )
