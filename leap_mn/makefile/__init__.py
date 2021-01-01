import os

from leap_mn.pkgdependency import PkgDependency
from moonleap import Resource, reduce


class Makefile(Resource):
    def __init__(self):
        self.rules = []

    def add_rule(self, rule):
        self.rules.append(rule)

    def describe(self):
        return dict(
            rules=[x for x in self.rules],
        )


class MakefileRule(Resource):
    def __init__(self, text):
        self.text = text

    def describe(self):
        return dict(text=self.text)


def create(term, block):
    return [Makefile(), PkgDependency("make", is_dev=True)]


@reduce(parent_resource=Makefile, resource=MakefileRule)
def add_makefile_rule(makefile, makefile_rule):
    if makefile_rule.is_created_in_block_that_mentions(makefile):
        makefile.add_rule(makefile_rule.text)


is_ittable = True
tags = ["makefile"]
render_function_by_resource_type = []
