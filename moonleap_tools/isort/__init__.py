from dataclasses import dataclass

from moonleap import add, rule, tags
from moonleap.verbs import uses
from moonleap_tools.pipdependency import PipDependency
from moonleap_tools.setupfile import SetupFileConfig
from moonleap_tools.tool import Tool

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

    add(isort, SetupFileConfig(setup_file_config))
    add(isort, PipDependency(["isort"], is_dev=True))

    return isort
