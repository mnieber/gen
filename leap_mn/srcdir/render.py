from pathlib import Path


def render_src_dir(src_dir, root_dir):
    p = Path(root_dir) / src_dir.location
    if not p.exists():
        p.mkdir()
