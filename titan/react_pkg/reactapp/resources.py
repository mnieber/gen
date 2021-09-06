import typing as T
from dataclasses import dataclass, field

from moonleap.resource import Resource
from titan.project_pkg.service import Tool


class ReactApp(Tool):
    pass


@dataclass
class ReactAppConfig(Resource):
    flags: T.Dict[str, T.Union[str, bool]] = field(default_factory=dict)
    index_imports: str = ""
    index_body: str = ""
