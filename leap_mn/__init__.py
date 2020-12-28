from moonleap.config import config, install
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
    install(dockercompose)
    install(dockerfile)
    install(gitrepository)
    install(layer)
    install(layergroup)
    install(layergroups)
    install(makefile)
    install(pipcompile)
    install(project)
    install(pytest)
    install(service)
    install(srcdir)


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
