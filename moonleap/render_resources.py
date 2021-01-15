from pathlib import Path

import jinja2
from jinja2 import Template
from jinja2_ansible_filters import AnsibleCoreFiltersExtension

from moonleap.config import config
from moonleap.render.load_template import load_template
from moonleap.render.template_renderer import TemplateRenderer


def _render(filename, resource):
    return Template(filename).render(res=resource)


def render_resources(blocks, output_root_dir):
    template_renderer = TemplateRenderer(output_root_dir)

    filenames = []
    for block in blocks:
        for resource in block.get_entities():
            if resource.block is not block:
                continue

            if hasattr(resource, "render"):
                resource.render(template_renderer)
                continue

            templates = _render(config.get_templates(resource), resource)

            if hasattr(resource, "output_paths"):
                output_sub_dir = resource.output_paths.merged.location
            else:
                output_sub_dir = ""

            if templates:
                for template_fn in Path(templates).glob("*"):
                    t = load_template(template_fn)
                    output_fn = _render(template_fn.name, resource)
                    output_dir = Path(output_root_dir) / output_sub_dir
                    output_dir.mkdir(parents=True, exist_ok=True)
                    fn = str(output_dir / output_fn)
                    if fn in filenames:
                        print(f"Warning: writing twice to {fn}")
                    else:
                        filenames.append(fn)

                    with open(fn, "w") as ofs:
                        ofs.write(t.render(res=resource))
