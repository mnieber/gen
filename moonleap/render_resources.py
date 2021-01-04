from pathlib import Path

from jinja2 import Template

from moonleap.config import config


def render_resources(blocks, root_dir):
    for block in blocks:
        for resource in block.get_resources():
            if getattr(resource, "name", "") == "config":
                resource.dump()

            templates = config.get_templates(resource.__class__)
            if templates:
                for template_fn in Path(templates).glob("*.*"):
                    with open(template_fn) as ifs:
                        t = Template(ifs.read(), trim_blocks=True)
                        output_fn = Template(template_fn.name).render(res=resource)

                        with open(str(Path(root_dir) / output_fn), "w") as ofs:
                            ofs.write(t.render(res=resource, project_name="TODO"))
