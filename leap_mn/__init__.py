from config import config, install
from ramda import merge

from . import (
    dockercompose,
    dockerfile,
    gitrepository,
    layer,
    layergroup,
    layergroups,
    makefile,
    pipcompile,
    project,
    pytest,
    service,
    srcdir,
)


def install_all():
    config.create_rule_by_tag = merge(
        config.create_rule_by_tag,
        {
            "docker-compose-dev": dockercompose.create_dev,
            "docker-compose": dockercompose.create,
            "docker-file-dev": dockerfile.create_dev,
            "docker-file": dockerfile.create,
            "dockerfile": dockerfile.create,
            "layer-group": layergroup.create,
            "layer": layer.create,
            "makefile": makefile.create,
            "pytest": pytest.create,
        },
    )

    config.ittable_lut = merge(
        config.ittable_lut,
        {
            "makefile": True,
            "layer-group": True,
            "service": True,
        },
    )


# config.update_rules = {
#     "pip-compile": [
#         leap_mn.pipcompile.add_to_makefile,
#         leap_mn.pipcompile.add_to_layer,
#     ],
#     "pytest": [
#         leap_mn.pytest.add_to_makefile,
#         leap_mn.pytest.add_to_layer,
#     ],
#     "pytest-html": [leap_mn.pytest.add_pytest_html],
#     "git-repository": [leap_mn.srcdir.set_git_repository],
#     "layer-group": [leap_mn.layergroup.add_layers],
#     "root-dir": [leap_mn.dockerfile.set_root_dir],
#     "src-mount-point": [leap_mn.dockerfile.set_src_mount_point],
# }
