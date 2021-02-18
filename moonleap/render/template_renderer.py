from pathlib import Path

import ramda as R
from jinja2 import Template
from moonleap.render.merge import get_file_merger
from moonleap.render.template_env import template_env


def _render_template(filename, resource):
    result = Template(filename).render(res=resource)
    if result.endswith(".j2"):
        result = result[:-3]
    return result


class TemplateRenderer:
    def __init__(self):
        self.filenames = []

    def render(self, output_root_dir, output_subdir, resource, template_fn):
        t = template_env.get_template(str(template_fn))
        output_fn = _render_template(template_fn.name, resource)

        output_dir = (Path(output_root_dir) / output_subdir).resolve()
        output_dir.mkdir(parents=True, exist_ok=True)
        fn = str(output_dir / output_fn)
        content = t.render(res=resource)

        if fn in self.filenames:
            file_merger = get_file_merger(fn)
            if file_merger:
                with open(fn) as ifs:
                    lhs_content = ifs.read()
                    content = file_merger.merge(lhs_content, content)
            else:
                print(f"Warning: writing twice to {fn}")
        else:
            self.filenames.append(fn)

        with open(fn, "w") as ofs:
            ofs.write(content)

        return fn


def merged_output_path(resource):
    from moonleap.resources.outputpath import OutputPath

    def _merge(acc, x):
        return OutputPath(location=(x.location + acc.location))

    merged = R.reduce(_merge, OutputPath(""), resource.output_paths.merged)
    return Path(merged.location)


def render_templates(root_filename, location="templates", output_subdir=None):
    def render(self, output_root_dir, template_renderer):
        output_filenames = []
        template_path = location(self) if callable(location) else location

        nonlocal output_subdir
        local_output_subdir = (
            output_subdir if output_subdir else merged_output_path(self)
        )

        templates_path = Path(root_filename).parent / template_path

        template_paths = (
            templates_path.glob("**/*") if templates_path.is_dir() else [templates_path]
        )

        def prepare(template_fn):
            return template_fn.relative_to(templates_path).parent

        for template_fn in template_paths:
            if not template_fn.is_dir():
                output_filenames.append(
                    template_renderer.render(
                        output_root_dir,
                        local_output_subdir / prepare(template_fn),
                        self,
                        template_fn,
                    )
                )

        return output_filenames

    return render
