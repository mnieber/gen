from moonleap import chop0
from moonleap_tools.makefile import MakefileRule


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
