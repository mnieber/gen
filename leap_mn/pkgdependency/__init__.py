from dataclasses import dataclass

import ramda as R
from moonleap import Resource


@dataclass
class PkgDependency(Resource):
    package_names: [str]
    is_dev: bool = False


def meta():
    return []
