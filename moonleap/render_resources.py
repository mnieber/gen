import os
from pathlib import Path

import jinja2
from jinja2 import Template
from jinja2_ansible_filters import AnsibleCoreFiltersExtension

from moonleap.config import config
from moonleap.utils import chop


def load_template(template_fn):
    with open(template_fn) as ifs:
        lines = [chop(x) for x in ifs.readlines()]

        state = "search loop"
        end_idx = len(lines)
        idx = len(lines) - 1

        while idx >= 0:
            line = lines[idx]

            if line.strip() == "":
                end_idx = idx

            if state == "search start":
                if line.strip().startswith(r"{% for") and line.strip().endswith(r"%}"):
                    lines.insert(idx + 1, "{% if loop.first %}")
                    state = "search loop"

            if state == "search loop":
                if line.strip() == r"{% body %}":
                    lines[idx] = r"{% endif %}"
                    lines.insert(end_idx, r"{% endfor %}")
                    state = "search start"

            idx -= 1

        new_text = os.linesep.join(lines)

        templateLoader = jinja2.FunctionLoader(lambda fn: new_text)
        templateEnv = jinja2.Environment(
            loader=templateLoader,
            extensions=[AnsibleCoreFiltersExtension],
            trim_blocks=True,
        )
        return templateEnv.get_template("tplt")


def _render(filename, resource):
    return Template(filename).render(res=resource)


def render_resources(blocks, output_root_dir):
    filenames = []
    for block in blocks:
        for resource in block.get_entities():
            if resource.block is not block:
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
