import os
from pathlib import Path

from moonleap.utils.case import sn
from titan.project_pkg.dockercompose import DockerComposeConfig


def _make_abs(service, p):
    result = Path(p)
    if not Path(os.path.expandvars(p)).is_absolute():
        base_path = Path("/opt") / sn(service.project.name) / service.name
        result = base_path / p
    return result


def get(opt_dir):
    def inner():
        service = opt_dir.service
        body = {}
        volumes = body.setdefault("volumes", [])
        for tool in service.tools:
            for opt_path in tool.opt_paths.merged:
                from_path = _make_abs(service, opt_path.from_path)
                to_path = _make_abs(service, opt_path.to_path)
                volumes.append(f"{str(from_path)}:{str(to_path)}")
        return body

    return DockerComposeConfig(
        get_service_body=lambda x, service_name: inner(),
        get_global_body=lambda x, service_name: {},
        is_dev=True,
        is_override=True,
    )
