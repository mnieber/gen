from moonleap import chop0
from moonleap_tools.makefile import MakefileRule


def get():
    return MakefileRule(
        chop0(
            """
pip-compile:
\tpip-compile requirements.in -o requirements.txt
\tpip-compile requirements.dev.in -o requirements.dev.txt

install:
\tpip install -r requirements.dev.txt
"""
        )
    )
