from dataclasses import dataclass

from titan.project_pkg.service import Tool


@dataclass
class Pytest(Tool):
    pass


@dataclass
class PytestHtml(Tool):
    pass
