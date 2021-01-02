from pathlib import Path


def render_docker_compose(docker_compose, root_dir):
    __import__("pudb").set_trace()
    p = Path(root_dir) / "src" / docker_compose.basename
    p.parent.mkdir(exist_ok=True)

    with open(str(p), "w") as ofs:
        ofs.write("version: 123")
