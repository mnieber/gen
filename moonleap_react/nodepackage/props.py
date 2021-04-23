import ramda as R
from moonleap.utils.merge_into_config import merge_into_config

from .resources import NodePackageConfig


def merge(lhs, rhs):
    new_body = dict()
    merge_into_config(new_body, lhs.get_body())
    merge_into_config(new_body, rhs.get_body())
    return NodePackageConfig(body=new_body)


def get_sort_index(key):
    lut = dict(
        name=1,
        version=2,
        private=3,
        dependencies=4,
        scripts=5,
        eslintConfig=6,
        browserslist=7,
    )

    return lut.get(key, 1000)


def get_node_package_config(self):
    service_configs = list(self.node_package_configs.merged)
    for module in self.service.modules:
        service_configs.extend(module.node_package_configs.merged)
    for tool in self.service.tools:
        service_configs.extend(tool.node_package_configs.merged)

    config = R.reduce(merge, NodePackageConfig(body={}), service_configs)
    result = R.pipe(
        R.always(config.get_body()),
        R.to_pairs,
        R.sort_by(lambda x: get_sort_index(x[0])),
        R.from_pairs,
    )(None)

    for k in ("dependencies", "devDependencies"):
        if result.get(k):
            result[k] = R.pipe(
                R.always(result[k]),
                R.to_pairs,
                R.sort_by(lambda x: x[0]),
                R.from_pairs,
            )(None)

    return result
