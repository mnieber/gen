from leaptools.makefile import MakefileRule
from moonleap import chop0


def get():
    return MakefileRule(
        chop0(
            """
        pip-compile:
        \tpip-compile requirements.in -o requirements.txt
        \tpip-compile requirements.dev.in -o requirements.dev.txt
        """
        )
    )
