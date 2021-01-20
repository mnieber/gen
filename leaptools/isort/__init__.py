from dataclasses import dataclass

from leaptools.pipdependency import PipDependency
from leaptools.setupfile import SetupFileConfig
from leaptools.tool import Tool
from moonleap import add, rule, tags
from moonleap.verbs import uses

setup_file_config = dict(
    isort=dict(
        multi_line_output=3,
        include_trailing_comma=True,
        force_grid_wrap=0,
        use_parentheses=True,
        line_length=88,
    )
)


@dataclass
class ISort(Tool):
    pass


@rule("service", uses, "isort")
def service_has_isort(service, isort):
    service.add_tool(isort)


@tags(["isort"])
def create_isort(term, block):
    isort = ISort()

    add(isort, SetupFileConfig(setup_file_config))
    add(isort, PipDependency(["isort"], is_dev=True))

    return isort
