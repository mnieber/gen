from moonleap import chop0
from titan.tools_pkg.makefile import MakefileRule


def get_run_server():
    return MakefileRule(
        name="run-server",
        text=chop0(
            """
run-server:
\tyarn start
"""
        ),
    )


def get_install():
    return MakefileRule(
        name="install",
        text=chop0(
            """
install:
\tyarn install
"""
        ),
    )
