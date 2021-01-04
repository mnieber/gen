import os

from leap_mn.pkgdependency import PkgDependency
from moonleap import Resource, tags


class Makefile(Resource):
    def __init__(self):
        super().__init__()
        self.rules = []

    def add_rule(self, rule):
        self.rules.append(rule)


class MakefileRule(Resource):
    def __init__(self, text):
        super().__init__()
        self.text = text


@tags(["makefile"])
def create(term, block):
    return [Makefile(), PkgDependency("make", is_dev=True)]


is_ittable = True
