from pathlib import Path


def _make_abs(service, p):
    base_path = Path("/opt") / service.project.name / service.name
    result = Path(p)
    if not result.is_absolute():
        result = base_path / p
    return result


def get(opt_dir):
    service = opt_dir.service
    body = {}
    volumes = body.setdefault("volumes", [])
    for tool in service.tools:
        for opt_path in tool.opt_paths.merged:
            from_path = _make_abs(service, opt_path.from_path)
            to_path = _make_abs(service, opt_path.to_path)
            volumes.append(f"{str(from_path)}:{str(to_path)}")
    return body
