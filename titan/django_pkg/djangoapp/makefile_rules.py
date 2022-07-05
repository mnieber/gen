from moonleap import chop0
from titan.tools_pkg.makefile import MakefileRule

body = chop0(
    """
run-server:
\tpython manage.py runserver 0.0.0.0:8000
"""
)


def get():
    return MakefileRule(name="run-server", text=body)
