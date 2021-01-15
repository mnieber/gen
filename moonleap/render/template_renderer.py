from pathlib import Path

from jinja2 import Template
from moonleap.render.load_template import load_template


def _render_template(filename, resource):
    return Template(filename).render(res=resource)


class TemplateRenderer:
    def __init__(self, output_root_dir):
        self.output_root_dir = output_root_dir
        self.filenames = []

    def render(self, output_subdir, resource, template_fn):
        t = load_template(template_fn)
        output_fn = _render_template(template_fn.name, self)
        output_dir = Path(self.output_root_dir) / output_subdir
        output_dir.mkdir(parents=True, exist_ok=True)
        fn = str(output_dir / output_fn)

        if fn in self.filenames:
            print(f"Warning: writing twice to {fn}")
        else:
            self.filenames.append(fn)

        with open(fn, "w") as ofs:
            ofs.write(t.render(res=resource))
