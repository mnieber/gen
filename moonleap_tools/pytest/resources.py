from dataclasses import dataclass

from moonleap_project.service import Tool


@dataclass
class Pytest(Tool):
    pass


@dataclass
class PytestHtml(Tool):
    pass
