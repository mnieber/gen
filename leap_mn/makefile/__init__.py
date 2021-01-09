import os

import moonleap.props as props
from leap_mn.layer import LayerConfig
from leap_mn.pkgdependency import PkgDependency, PkgDependencyDev
from leap_mn.service import Service
from moonleap import Resource, output_dir_from, tags


class Makefile(Resource):
    def __init__(self):
        super().__init__()

    def add_rule(self, rule):
        self.rules.append(rule)


class MakefileRule(Resource):
    def __init__(self, text):
        super().__init__()
        self.text = text


def get_layer_config():
    return dict(decorators=dict(docker=["make"]))


@tags(["makefile"])
def create_makefile(term, block):
    return [
        Makefile(),
        PkgDependencyDev(["make"]),
        LayerConfig("root", get_layer_config()),
    ]


meta = {
    Makefile: dict(
        templates="templates",
        output_dir=output_dir_from("service"),
        props={
            "rules": props.children_of_type(MakefileRule),
            "service": props.parent_of_type(Service),
        },
    )
}
