import os
from pathlib import Path

import ramda as R
from jinja2 import Template
from moonleap.render.merge import get_file_merger
from moonleap.render.template_env import template_env


def merged_output_path(resource):
    from moonleap.resources.outputpath import OutputPath

    def _merge(acc, x):
        return OutputPath(location=(x.location + acc.location))

    merged = R.reduce(_merge, OutputPath(""), resource.output_paths.merged)
    return Path(merged.location)


class TemplateRenderer:
    def __init__(self):
        self.filenames = []

    def render(self, resource, template_fn, fn):
        if template_fn.suffix == ".j2":
            template = template_env.get_template(str(template_fn))
            content = template.render(res=resource)
        else:
            with open(template_fn) as ifs:
                content = ifs.read()

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


def _get_output_dir(output_root_dir, output_subdir, templates_path, template_fn):
    return (
        Path(output_root_dir)
        / output_subdir
        / template_fn.relative_to(templates_path).parent
    ).resolve()


def _get_output_fn(output_dir, resource, template_fn):
    meta_filename = str(template_fn) + ".fn"
    if Path(meta_filename).exists():
        fn = (
            template_env.get_template(meta_filename)
            .render(res=resource)
            .split(os.linesep)[0]
        )
    else:
        fn = Template(template_fn.name).render(res=resource)
        if fn.endswith(".j2"):
            fn = fn[:-3]
    return str(output_dir / fn)


def render_templates(root_filename, location="templates", output_subdir=None):
    def render(resource, output_root_dir, template_renderer):
        nonlocal output_subdir

        template_path = location(resource) if callable(location) else location
        templates_path = Path(root_filename).parent / template_path
        template_paths = (
            templates_path.glob("**/*") if templates_path.is_dir() else [templates_path]
        )

        output_filenames = []
        for template_fn in template_paths:
            if template_fn.suffix == ".fn":
                continue
            if not template_fn.is_dir():
                output_dir = _get_output_dir(
                    output_root_dir,
                    output_subdir or merged_output_path(resource),
                    templates_path,
                    template_fn,
                )
                output_dir.mkdir(parents=True, exist_ok=True)

                output_filename = template_renderer.render(
                    resource,
                    template_fn,
                    _get_output_fn(output_dir, resource, template_fn),
                )
                output_filenames.append(output_filename)
        return output_filenames

    return render
