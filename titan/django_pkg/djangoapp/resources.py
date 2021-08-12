from dataclasses import dataclass

from moonleap import Resource
from titan.project_pkg.service import Tool


@dataclass
class DjangoApp(Tool):
    pass


@dataclass
class DjangoConfig(Resource):
    values: dict
