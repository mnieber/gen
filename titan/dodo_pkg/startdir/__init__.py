from pathlib import Path

from moonleap import rule


@rule("config:layer")
def add_start_dir(layer):
    layer.add_template_dir(Path(__file__).parent / "templates")
