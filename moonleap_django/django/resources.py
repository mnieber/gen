from dataclasses import dataclass

from moonleap import Resource
from moonleap_project.service import Tool


@dataclass
class Django(Tool):
    pass


@dataclass
class DjangoConfig(Resource):
    values: dict
