import moonleap.props as props
import moonleap.rules as rules
from moonleap import Resource, tags


class Project(Resource):
    def __init__(self, name):
        super().__init__()
        self.name = name


@tags(["project"])
def create_project(term, block):
    return Project(term.data)


def meta():
    from leap_mn.service import Service
    from leap_mn.srcdir import SrcDir

    return {
        Project: dict(
            output_dir="src",
            props={
                "services": props.children_of_type(Service),
                "src_dir": props.child_of_type(SrcDir),
            },
        )
    }


rules = {
    "project": {
        ("has", "service"): rules.add_child,
        ("has", "src_dir"): rules.add_child,
    }
}
