from moonleap import chop0
from titan.tools_pkg.makefile import MakefileRule


def get_pipcompile():
    return MakefileRule(
        name="pip-compile",
        text=chop0(
            """
pip-compile:
\tpip-compile requirements.in -o requirements.txt
\tpip-compile requirements.dev.in -o requirements.dev.txt
"""
        ),
    )


def get_install():
    return MakefileRule(
        name="install",
        text=chop0(
            """
install:
\tpip install -r requirements.dev.txt
"""
        ),
    )
