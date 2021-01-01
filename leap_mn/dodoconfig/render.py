from pathlib import Path

import ramda as R
from yaml import dump


def render_layer(layer, root_dir):
    with open(str(Path(root_dir) / layer.path), "w") as ofs:
        for section in R.sort_by(R.prop("name"))(layer.sections):
            ofs.write(dump(section.config))
