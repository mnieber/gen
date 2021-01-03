import os

from leap_mn.pkgdependency import PkgDependency
from moonleap import Resource


class Makefile(Resource):
    def __init__(self):
        self.rules = []

    def add_rule(self, rule):
        self.rules.append(rule)

    def describe(self):
        return dict(
            rules=[x for x in self.rules],
        )


def create(term, block):
    return [Makefile(), PkgDependency("make", is_dev=True)]


is_ittable = True
tags = ["makefile"]
