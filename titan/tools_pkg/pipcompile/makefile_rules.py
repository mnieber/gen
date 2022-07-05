from moonleap import chop0
from titan.tools_pkg.makefile import MakefileRule


def get_pipcompile():
    return MakefileRule(
        name="pip-compile",
        text=chop0(
            """
pip-compile:
\tpip-compile requirements.base.in -o requirements.base.txt
\tpip-compile requirements.dev.in -o requirements.dev.txt
\tpip-compile requirements.prod.in -o requirements.prod.txt
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
