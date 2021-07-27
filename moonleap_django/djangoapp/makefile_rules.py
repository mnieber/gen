from moonleap import chop0
from moonleap_tools.makefile import MakefileRule


def get():
    return MakefileRule(
        chop0(
            """
runserver:
\tpython manage.py runserver 0.0.0.0:8000 --nostatic

"""  # noqa
        )
    )
