from pathlib import Path

import ramda as R
from jinja2 import Template
from moonleap.render.load_template import load_template
from moonleap.resource.memfun import MemFun


def _render_template(filename, resource):
    return Template(filename).render(res=resource)


class TemplateRenderer:
    def __init__(self):
        self.filenames = []

    def render(self, output_root_dir, output_subdir, resource, template_fn):
        t = load_template(template_fn)
        output_fn = _render_template(template_fn.name, resource)
        output_dir = Path(output_root_dir) / output_subdir
        output_dir.mkdir(parents=True, exist_ok=True)
        fn = str(output_dir / output_fn)

        if fn in self.filenames:
            print(f"Warning: writing twice to {fn}")
        else:
            self.filenames.append(fn)

        with open(fn, "w") as ofs:
            ofs.write(t.render(res=resource))


def merged_output_path(output_paths):
    from moonleap.resources.outputpath import OutputPath

    def _merge(acc, x):
        return OutputPath(location=(x.location + acc.location))

    return R.reduce(_merge, OutputPath(""), output_paths)


def render_templates(root_filename, location="templates"):
    def render(self, output_root_dir, template_renderer):
        template_path = location(self) if callable(location) else location

        output_path = merged_output_path(self.output_paths.merged)
        output_sub_dir = output_path.location
        templates_path = Path(root_filename).parent / template_path

        template_paths = (
            templates_path.glob("**/*") if templates_path.is_dir() else [templates_path]
        )

        def prepare(template_fn):
            result = template_fn.relative_to(templates_path).parent
            return Path(str(result).replace("/parentdir/", "/../")).resolve()

        for template_fn in template_paths:
            if not template_fn.is_dir():
                template_renderer.render(
                    output_root_dir,
                    output_sub_dir / prepare(template_fn),
                    self,
                    template_fn,
                )

    return MemFun(render)
