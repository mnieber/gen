from dataclasses import dataclass

from moonleap import Resource


@dataclass
class PipDependency(Resource):
    package_names: [str]
    is_dev: bool = False
