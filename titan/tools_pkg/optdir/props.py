import os
from pathlib import Path


def render_opt_dir(opt_dir, write_file, **kwargs):
    service = opt_dir.service
    if service:
        for tool in service.tools:
            for opt_path in tool.opt_paths.merged:
                from_path = os.path.expandvars(opt_path.from_path)
                if not Path(from_path).is_absolute():
                    p = Path("opt") / service.name / from_path
                    if opt_path.is_dir:
                        write_file(p, None, is_dir=True)
                    else:
                        write_file(p, "")
