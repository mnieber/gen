import os

from leap_mn.pkgdependency import PkgDependency
from moonleap import Resource


class Makefile(Resource):
    def __init__(self):
        super().__init__()
        self.rules = []

    def add_rule(self, rule):
        self.rules.append(rule)

    def describe(self):
        return dict(
            rules=[x for x in self.rules],
        )


class MakefileRule(Resource):
    def __init__(self, text):
        super().__init__()
        self.text = text

    def describe(self):
        return dict(text=self.text)


def create(term, block):
    return [Makefile(), PkgDependency("make", is_dev=True)]


is_ittable = True
tags = ["makefile"]
