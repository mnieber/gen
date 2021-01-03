from pathlib import Path

from jinja2 import Template

from moonleap.config import config


def render_resources(blocks, root_dir):
    for block in blocks:
        for resource in block.get_resources():
            templates = config.templates_by_resource_type_id.get(resource.type_id)
            if templates:
                __import__("pudb").set_trace()
                for template_fn in Path(templates).glob("*.*"):
                    with open(template_fn) as ifs:
                        t = Template(ifs.read())
                        output_fn = Template(template_fn.name).render(res=resource)

                        with open(str(Path(root_dir) / output_fn), "w") as ofs:
                            ofs.write(t.render(res=resource))

            render = config.render_function_by_resource_type_id.get(resource.type_id)
            if render:
                render(resource, root_dir)
