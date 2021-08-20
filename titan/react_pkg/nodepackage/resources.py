import typing as T
from dataclasses import dataclass
from pathlib import Path

from moonleap.resource import Resource
from moonleap.utils import yaml2dict
from titan.project_pkg.service import Tool


@dataclass
class NodePackage(Tool):
    pass


@dataclass
class NodePackageConfig(Resource):
    body: T.Union[dict, T.Callable]

    def get_body(self):
        return self.body(self) if callable(self.body) else self.body


def load_node_package_config(root_fn):
    fn = Path(root_fn).parent / "package.json"
    with open(fn) as ifs:
        return NodePackageConfig(body=yaml2dict(ifs.read()))
