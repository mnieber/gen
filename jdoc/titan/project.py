from jdoc.titan.imports import *
from jdoc.titan.service import *


class ProjectRes(Resource):
    name: str
    services: T.List[ServiceRes] = []
