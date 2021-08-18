from moonleap import chop0
from titan.tools_pkg.makefile import MakefileRule


def get():
    return MakefileRule(
        name="runserver",
        text=chop0(
            """
runserver:
\tpython manage.py runserver 0.0.0.0:8000

"""  # noqa: E501
        ),
    )
