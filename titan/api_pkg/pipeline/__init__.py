from moonleap import create

from .resources import LocalVars, PropsSource


@create("props")
def create_props(term):
    return PropsSource()


@create("local:vars")
def create_local_vars(term):
    return LocalVars()
