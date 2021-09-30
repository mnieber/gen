from dataclasses import dataclass

from moonleap import add, create
from titan.project_pkg.service import Tool
from titan.tools_pkg.pipdependency import PipDependency
from titan.tools_pkg.setupfile import SetupFileConfig

setup_file_config = dict(
    isort=dict(
        multi_line_output=3,
        include_trailing_comma=True,
        force_grid_wrap=0,
        use_parentheses=True,
        line_length=88,
    )
)


base_tags = [("isort", ["tool"])]


@dataclass
class ISort(Tool):
    pass


@create("isort")
def create_isort(term, block):
    isort = ISort(name="isort")

    add(isort, SetupFileConfig(setup_file_config))
    add(isort, PipDependency(["isort"], is_dev=True))

    return isort
