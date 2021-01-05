from pathlib import Path

from jinja2 import Template

from moonleap.config import config


def render_resources(blocks, root_dir):
    for block in blocks:
        for resource in block.get_resources():
            print(resource)

            templates = config.get_templates(resource.__class__)
            output_sub_dir = config.get_output_dir(resource) or ""

            if templates:
                for template_fn in Path(templates).glob("*"):
                    with open(template_fn) as ifs:
                        t = Template(ifs.read(), trim_blocks=True)
                        output_fn = Template(template_fn.name).render(res=resource)
                        output_dir = Path(root_dir) / output_sub_dir
                        output_dir.mkdir(exist_ok=True)

                        with open(str(output_dir / output_fn), "w") as ofs:
                            ofs.write(t.render(res=resource, project_name="TODO"))
