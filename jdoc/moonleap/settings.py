from jdoc.moonleap.imports import *
from jdoc.moonleap.package import *


class EntryPoint(Entity):
    pass


class Settings(Entity):
    scope_by_name = {}
    post_process = {}
    bin = {}
