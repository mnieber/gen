from dataclasses import dataclass

from leap_mn.pipdependency import PipDependency
from leap_mn.setupfile import SetupFileConfig
from leap_mn.tool import Tool
from moonleap import tags

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


@tags(["isort"])
def create_isort(term, block):
    isort = ISort()
    isort.setup_file_configs.add(SetupFileConfig(setup_file_config))
    isort.pip_dependencies.add(PipDependency(["isort"], is_dev=True))
    return isort
