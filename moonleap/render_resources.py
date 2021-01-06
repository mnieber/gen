import os
from pathlib import Path

from jinja2 import Template

from moonleap.config import config
from moonleap.utils import chop


def load_template(template_fn):
    with open(template_fn) as ifs:
        lines = [chop(x) for x in ifs.readlines()]

        state = "search loop"
        offset = 0
        end_idx = len(lines)
        idx = len(lines) - 1
        for_statement = None

        while idx >= 0:
            line = lines[idx]

            if line.strip() == "":
                end_idx = idx
                if state == "search start":
                    lines.insert(idx + 1, for_statement)
                    lines.insert(idx + 2, "{% if loop.first %}")
                    state = "search loop"

            if line.strip().startswith(r"{% loop") and line.strip().endswith(r"%}"):
                for_statement = line.replace(r"{% loop", r"{% for")
                lines[idx] = r"{% endif %}"
                lines.insert(end_idx, r"{% endfor %}")
                state = "search start"

            idx -= 1

        new_text = os.linesep.join(lines)
        return Template(new_text, trim_blocks=True)


def render_resources(blocks, output_root_dir):
    for block in blocks:
        for resource in block.get_resources():
            print(resource)

            templates = config.get_templates(resource.__class__)
            output_sub_dir = config.get_output_dir(resource) or ""

            if templates:
                for template_fn in Path(templates).glob("*"):
                    t = load_template(template_fn)
                    output_fn = Template(template_fn.name).render(res=resource)
                    output_dir = Path(output_root_dir) / output_sub_dir
                    output_dir.mkdir(parents=True, exist_ok=True)

                    with open(str(output_dir / output_fn), "w") as ofs:
                        ofs.write(t.render(res=resource, project_name="TODO"))
