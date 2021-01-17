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
