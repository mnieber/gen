from pathlib import Path


def render_opt_dir(opt_dir, output_root_dir, **kwargs):
    service = opt_dir.service
    if service:
        for tool in service.tools:
            for opt_path in tool.opt_paths.merged:
                if not Path(opt_path.from_path).is_absolute():
                    p = (
                        Path(output_root_dir)
                        / "opt"
                        / service.name
                        / opt_path.from_path
                    )
                    p.parent.mkdir(parents=True, exist_ok=True)
                    p.touch()


def get_docker_compose_config(opt_dir):
    volumes = []
    service = opt_dir.service
    project = service.project
    base_path = Path("/opt") / project.name / service.name

    def make_abs(p):
        result = Path(p)
        if not result.is_absolute():
            result = base_path / p
        return result

    if service:
        for tool in service.tools:
            for opt_path in tool.opt_paths.merged:
                from_path = make_abs(opt_path.from_path)
                to_path = make_abs(opt_path.to_path)
                volumes.append(f"{str(from_path)}:{str(to_path)}")

    return {service.name: {"volumes": volumes}}
